# Transfer data( include create tables, pk and fk's) from MySQL to SQL Server 08.04.2023 
import pyodbc
import datetime
from sqlalchemy import create_engine
import pandas as pd
import pymysql

# MySQL connection env. 
db_user = <some>
db_password = <some>
db_host = <some>
db_port = <some>
db_name = <some>

# Connect to MySQL database
cnx_mysql = pymysql.connect(user=db_user, password=db_password,
                             host=db_host, port=int(db_port), db=db_name)

# Connect to SQL Server database
cnx_sql = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                          'SERVER=<some>;'
                          'DATABASE=<some>;'
                          'UID=sa;'
                          'PWD=<some>')

# Set up SQLAlchemy engine for SQL Server connection
engine_sql = create_engine('mssql+pyodbc://sa:<some>@<some>/<some>?driver=ODBC+Driver+17+for+SQL+Server')
# Get all table names from MySQL database
cursor_mysql = cnx_mysql.cursor()
cursor_mysql.execute("SHOW TABLES")
tables = cursor_mysql.fetchall()

# Iterate over each table and transfer data
for table in tables:
    table_name = table[0]

    # Check if table exists in SQL Server database
    cursor_sql = cnx_sql.cursor()
    cursor_sql.execute(f"SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{table_name}'")
    table_exists = len(cursor_sql.fetchall()) > 0
    
    if not table_exists:
        # Fetch column names and data types from MySQL table
        cursor_mysql.execute(f"DESCRIBE {table_name}")
        columns = cursor_mysql.fetchall()
        columns_sql = [f"{col[0].replace('İ', 'I')} {'float' if 'double' in col[1] else col[1].replace('tinyint(1)', 'tinyint')}" for col in columns]

        cursor_mysql.execute(f"SHOW INDEX FROM {table_name}")
        indexes = cursor_mysql.fetchall()
        pk_cols = [idx[4] for idx in indexes if idx[2] == 'PRIMARY']
        if len(pk_cols) > 0:
            pk_constraint = f", CONSTRAINT PK_{table_name} PRIMARY KEY ({','.join(pk_cols)})"
        else:
            pk_constraint = ''
        index_cols = [idx[4] for idx in indexes if idx[2] != 'PRIMARY']
        if len(index_cols) > 0:
            index_constraints = [f"INDEX IX_{table_name}_{col} ({col})" for col in index_cols]
            index_constraint = f", {','.join(index_constraints)}"
        else:
            index_constraint = ''
        
        
        # Generate SQL statement to create table in SQL Server
        query = f"CREATE TABLE {table_name} ({','.join(columns_sql)}{pk_constraint}{index_constraint})"
        print(query) # print the generated query

        # Execute query to create table in SQL Server database
        cursor_sql.execute(query)
        cursor_sql.commit()
    cursor_sql.close()

    # Fetch latest timestamp from SQL Server table
    latest_timestamp = pd.read_sql(f"SELECT MAX(createdAt) FROM {table_name}", engine_sql).iloc[0,0]
    if pd.isna(latest_timestamp):
        latest_timestamp = datetime.datetime.min

    # Fetch data from MySQL table that has been updated since the last copy
    chunk_size = 10000 # number of rows to read at a time
    offset = 0
    while True:
        start_time = datetime.datetime.now()
        query = f"SELECT * FROM {table_name} WHERE createdAt > '{latest_timestamp}' LIMIT {chunk_size} OFFSET {offset}"
        data = pd.read_sql(query, cnx_mysql)

        # If there is no more data to read
        if len(data) == 0:
            break

        # Write data to SQL Server table
        try:
            data.to_sql(name=table_name, con=engine_sql, if_exists='append', index=False)
            end_time = datetime.datetime.now()
            elapsed_time = end_time - start_time
            elapsed_seconds = int(elapsed_time.total_seconds())
            minutes, seconds = divmod(elapsed_seconds, 60)
            print(f"Data transfer for table {table_name} ; {len(data)} rows was successful in: {minutes} minutes {seconds} seconds.")
        except Exception as e:
            print(f"Data transfer for table {table_name} failed with error: {str(e)}")

        # Increment offset for next chunk of data
        offset += chunk_size

# Close database connections
cnx_mysql.close()
engine_sql.dispose()
