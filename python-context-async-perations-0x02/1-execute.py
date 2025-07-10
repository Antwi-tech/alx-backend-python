import sqlite3

# Reusable context manager for executing a SQL query
class ExecuteQuery:
    def __init__(self, db_name, query, params=None):
        self.db_name = db_name      # Database file name
        self.query = query          # SQL query to be executed
        self.params = params or ()  # Parameters for the query
        self.connection = None      # Database connection
        self.cursor = None          # Cursor object
        self.results = None         # Query results

    def __enter__(self):
        # Open connection and create cursor
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()

        # Execute the query with parameters
        self.cursor.execute(self.query, self.params)

        # Fetch results immediately
        self.results = self.cursor.fetchall()
        return self.results  # Return the query results to the with-block

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Ensure cursor and connection are closed properly
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        # You can return False to propagate exceptions if any occurred

# Example usage: fetch users older than 25
query = "SELECT * FROM users WHERE age > ?"
params = (25,)

# Use the context manager to execute the query
with ExecuteQuery('users.db', query, params) as results:
    print("Users older than 25:")
    for row in results:
        print(row)


        """
        Here’s how you can implement a reusable class-based context manager named ExecuteQuery that:

Takes a SQL query and optional parameters.

Opens the database connection.

Executes the query with parameters.

Returns the result.

Automatically handles connection and cursor cleanup using __enter__() and __exit__().

 Key Notes:
params is passed as a tuple to prevent SQL injection and support parameterized queries.

results is fetched and returned from __enter__(), making the context block simple and clean.

Proper cleanup is handled in __exit__() whether or not an error occurs.
        """