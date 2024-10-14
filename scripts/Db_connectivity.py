import pyodbc

def connect_to_db(DATABASE_NAME):
    try:
        # Connection string for Microsoft SQL Server
        conn = pyodbc.connect(
            'DRIVER={SQL Server};'
            'SERVER=PUFF10\\MARUSQL;'
            f'DATABASE={DATABASE_NAME};'
            'Trusted_Connection=yes;'
            'UID=PUFF10\\maru;'
            'PWD=maru0927;'
        )
        print("Connection to Microsoft SQL Server established successfully.")
        return conn
    except Exception as e:
        print(f"Error connecting to database: {str(e)}")
        return None
