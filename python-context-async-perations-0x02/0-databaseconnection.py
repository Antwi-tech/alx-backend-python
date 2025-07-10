import sqlite3

# Class-based context manager for database connections
class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name  # Name of the database file
        self.connection = None  # Placeholder for the connection object

    def __enter__(self):
        # Open the database connection when entering the context
        self.connection = sqlite3.connect(self.db_name)
        return self.connection  # Return the connection so it can be used inside the with-block

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Automatically close the connection when exiting the context
        if self.connection:
            self.connection.close()

# Use the custom context manager to query the users table
with DatabaseConnection('users.db') as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")  # Perform query
    results = cursor.fetchall()            # Fetch all results

    # Print the results
    print("Users in the database:")
    for user in results:
        print(user)
