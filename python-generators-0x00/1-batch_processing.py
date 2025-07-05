import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Generator function to fetch users in batches from the database
def stream_users_in_batches(batch_size):
    # Establish connection to the MySQL database
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password=os.getenv("MYSQL_ROOT_PASSWORD"),
        database='ALX_prodev'
    )
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    batch = []  # Initialize an empty batch list
    for row in cursor:
        batch.append(row)  # Add each row to the batch
        if len(batch) == batch_size:
            yield batch  # Yield the batch when it reaches the desired size
            batch = []  # Reset the batch

    if batch:
        yield batch  # Yield the last batch if it's not empty

    # Close cursor and connection
    cursor.close()
    connection.close()

# Function to process batches and print users older than 25
def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if int(user['age']) > 25:
                print(user)  # Print user data if age is greater than 25
