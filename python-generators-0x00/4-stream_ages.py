#!/usr/bin/python3
import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Generator function to stream ages one by one
def stream_user_ages():
    # Connect to MySQL
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password=os.getenv("MYSQL_ROOT_PASSWORD"),
        database='ALX_prodev'
    )
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data")

    # Yield each age
    for (age,) in cursor:
        yield float(age)

    cursor.close()
    connection.close()

# Function to calculate average using the generator
def compute_average_age():
    total = 0
    count = 0
    for age in stream_user_ages():
        total += age
        count += 1

    # Print average age (avoids division by zero)
    if count > 0:
        print(f"Average age of users: {total / count:.2f}")
    else:
        print("No users found.")

# Run the function
compute_average_age()
