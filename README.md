# Transfer data from MySQL to SQL Server

This Python script performs the transfer of data from a MySQL database to a SQL Server database. Here is a summary of the script:

### Prerequisites
  - Python 3.7 or higher
  - pyodbc module
  - sqlalchemy module
  - pandas module
  - pymysql module
  - MySQL database
  - SQL Server database

### Usage
1. Install the required modules using pip:
``` 
pip install mysql-connector-python pyodbc sqlalchemy pandas pymysql 
```

2. Set the MySQL and SQL Server connection parameters in the script:

 ```
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
 ```

3. Run the script:
``` 
python mysql_to_sqlserver.py 
```

## Functionality
1. The script fetches all table names from the MySQL database.
2. For each table;
  - It checks if the table exists in the SQL Server database.
  - If the table does not exist, it creates it in the SQL Server database with the same columns, data types, and indexes as in the MySQL table.
  -  It fetches the latest timestamp from the SQL Server table.
  -  It fetches the data from the MySQL table that has been updated since the last copy and writes it to the SQL Server table.
  -  It prints the number of rows transferred and the elapsed time for the transfer.

## Notes
  - The script assumes that the primary key and index constraints in the MySQL table are named using the following convention: PRIMARY KEY constraint is named PRIMARY, and each index constraint is named IX_tablename_columnname.
  - The script uses pandas to read data from MySQL and write data to SQL Server. Therefore, it may not be suitable for transferring large amounts of data.
  - The script does not handle any schema changes in the MySQL table. If the schema of the MySQL table changes, the SQL Server table needs to be recreated manually, and the data needs to be transferred again.
