import mysql.connector
import csv
import os
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from a .env file


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


def create_database(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
    connection.commit()
    cursor.close()


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


def create_table(connection):
    cursor = connection.cursor()

    # Drop the table if it exists to ensure fresh schema
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


def insert_data(connection, csv_filename):
    cursor = connection.cursor()
    with open(csv_filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Check if the email already exists to avoid duplicates
            cursor.execute("SELECT email FROM user_data WHERE email = %s", (row['email'],))
            if cursor.fetchone():
                continue  # Skip if already exists
            cursor.execute(
                "INSERT INTO user_data (name, email, age) VALUES (%s, %s, %s)",
                (row['name'], row['email'], row['age'])
            )
    connection.commit()
    cursor.close()
