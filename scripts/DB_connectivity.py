import psycopg2

def connect_to_db(DATABASE_NAME):
    try:
        # Connection string for PostgreSQL
        conn = psycopg2.connect(
            dbname='ethiomedical_info',
            user='postgres',        # Replace with your PostgreSQL username (default is usually 'postgres')
            password='Maru@132',    # Replace with your PostgreSQL password
            host='localhost',       # Replace with your host (default is usually 'localhost')
            port='5432'             # Replace with your port (default for PostgreSQL is '5432')
        )
        print("Connection to PostgreSQL database established successfully.")
        return conn
    except Exception as e:
        print(f"Error connecting to database: {str(e)}")
        return None
