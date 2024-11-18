import pandas as pd
import logging
import psycopg2
from DB_connectivity import connect_to_db

# Set up logging
logging.basicConfig(filename='data_cleaning.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

DATABASE_NAME = 'ethiomedical_info'  # Replace with your database name
TABLE_NAME = 'medical_info'  # Define the table name

# Load data
def load_data(file_path):
    try:
        # Load the dataset into a pandas DataFrame
        data = pd.read_csv(file_path)
        logging.info("Data loaded successfully.")
        return data
    except Exception as e:
        logging.error(f"Error loading data: {str(e)}")
        return None

# Clean data
def clean_data(df):
    try:
        # Rename columns to match the SQL table
        df.rename(columns={
            'Channel Title': 'Channel_Title',
            'Channel Username': 'Channel_Username',
            'ID': 'ID',
            'Message': 'Message',
            'Date': 'Date',
            'Media Path': 'Media_Path'
        }, inplace=True)

        # Remove duplicates
        df = df.drop_duplicates()
        logging.info("Duplicates removed.")
        
        # Handle missing values (Example: fill with 'Unknown' for text columns)
        df.fillna('Unknown', inplace=True)
        logging.info("Missing values handled.")
        
        # Standardize formats (Example: convert all text to lowercase)
        df = df.applymap(lambda s: s.lower() if isinstance(s, str) else s)
        logging.info("Data formats standardized.")

        # Data validation
        if df.isnull().values.any():
            logging.warning("Data still contains missing values after cleaning.")
        
        return df
    except Exception as e:
        logging.error(f"Error cleaning data: {str(e)}")
        return None

# Create table if it does not exist
def create_table_if_not_exists(conn):
    try:
        cursor = conn.cursor()
        
        # Define the SQL column types based on DataFrame columns
        column_definitions = [
            "Channel_Title TEXT",
            "Channel_Username TEXT",
            "ID TEXT",
            "Message TEXT",
            "Date TEXT",
            "Media_Path TEXT"
        ]

        # Join column definitions to create the table statement
        column_definitions_str = ", ".join(column_definitions)
        create_table_sql = f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} ({column_definitions_str});

        
        cursor.execute(create_table_sql)
        conn.commit()
        logging.info(f"Table '{TABLE_NAME}' checked/created successfully.")
    except Exception as e:
        logging.error(f"Error creating table: {str(e)}")
    finally:
        cursor.close()

# Store data into database
def store_data(df):
    try:
        # Connect to PostgreSQL database
        conn = connect_to_db(DATABASE_NAME)
        if conn is None:
            logging.error("Failed to connect to database. Exiting storage process.")
            return

        # Create the table if it does not exist
        create_table_if_not_exists(conn)

        # Insert data into the table
        cursor = conn.cursor()
        for index, row in df.iterrows():
            # Prepare the SQL INSERT statement dynamically
            placeholders = ", ".join(["%s"] * len(row))
            column_names = ", ".join([f"{col}" for col in df.columns])
            insert_sql = f"INSERT INTO {TABLE_NAME} ({column_names}) VALUES ({placeholders})"
            cursor.execute(insert_sql, tuple(row))
        conn.commit()
        logging.info("Data stored in database successfully.")
        
        cursor.close()
        conn.close()
    except Exception as e:
        logging.error(f"Error storing data: {str(e)}")

# Main function which calls all functions
def main():
    file_path = 'C:/Users/User/Desktop/Github/Data_Warehouse_ForEthioMedical/telegram_data.csv'  

    # Load, clean, and store data
    df = load_data(file_path)
    if df is not None:
        cleaned_df = clean_data(df)
        if cleaned_df is not None:
            store_data(cleaned_df)

if __name__ == "__main__":
    main()
