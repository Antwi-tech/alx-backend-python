# 0-stream_users.py
from itertools import islice
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def stream_users():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password=os.getenv("MYSQL_ROOT_PASSWORD"),
        database='ALX_prodev'
    )
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    for row in cursor:
        yield row

    cursor.close()
    connection.close()
    
for user in islice(stream_users(), 6):
    print(user)
