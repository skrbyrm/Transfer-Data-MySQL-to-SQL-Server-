# Transfer Data MySQL-to-SQL-Server 

### This Python script performs the transfer of data from a MySQL database to a SQL Server database. Here is a summary of the script:

- Imports required packages, including mysql.connector, pyodbc, datetime, and pandas.
- Sets up the MySQL database connection environment by specifying the user, password, host, port, and database name.
- Connects to the MySQL database using the connection information provided in step 2.
- Sets up the SQL Server database connection environment by specifying the driver, server, database, user ID, and password.
- Sets up a SQLAlchemy engine to connect to the SQL Server database.
- Gets a list of all table names in the MySQL database.
- Iterates over each table in the MySQL database.
- Checks if the table exists in the SQL Server database. If not, creates the table using the column names and data types fetched from the MySQL table.
- Fetches the latest timestamp from the SQL Server table for the current table. If no timestamp is found, sets the latest timestamp to datetime.datetime.min.
- Fetches the data from the MySQL table that has been updated since the latest timestamp.
- Writes the fetched data to the SQL Server table in chunks of 10000 rows.
- Closes the database connections.
- The script prints out relevant information at various stages of the transfer process. Overall, the script is designed to automate the process of transferring data from   a MySQL database to a SQL Server database.
