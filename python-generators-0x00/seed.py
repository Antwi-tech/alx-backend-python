import mysql.connector
import csv
import os
from mysql.connector import Error
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Function to connect to the MySQL server
def connect_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password=os.getenv("MYSQL_ROOT_PASSWORD")
        )
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

# Function to create the ALX_prodev database if it does not exist
def create_database(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
    connection.commit()
    cursor.close()

# Function to connect directly to the ALX_prodev database
def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password=os.getenv("MYSQL_ROOT_PASSWORD"),
            database='ALX_prodev'
        )
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

# Function to create the user_data table
def create_table(connection):
    cursor = connection.cursor()

    # Drop the table if it exists to avoid schema conflicts
    cursor.execute("DROP TABLE IF EXISTS user_data;")

    create_table_query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) NOT NULL,
        age DECIMAL NOT NULL
    );
    """
    cursor.execute(create_table_query)
    connection.commit()
    cursor.close()
    print("Table user_data created successfully")

# Function to insert user data from a CSV file into the user_data table
def insert_data(connection, csv_filename):
    cursor = connection.cursor()
    with open(csv_filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Check if the email already exists to avoid inserting duplicates
            cursor.execute("SELECT email FROM user_data WHERE email = %s", (row['email'],))
            if cursor.fetchone():
                continue  # Skip duplicate email

            # Insert new row into the table
            cursor.execute(
                "INSERT INTO user_data (name, email, age) VALUES (%s, %s, %s)",
                (row['name'], row['email'], row['age'])
            )
    connection.commit()
    cursor.close()
