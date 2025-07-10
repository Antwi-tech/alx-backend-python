import sqlite3
import functools
from datetime import datetime  # Importing datetime for timestamp logging

# Decorator to log SQL queries with timestamps
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract the query either from keyword args or positional args
        query = kwargs.get('query', args[0] if args else 'UNKNOWN QUERY')
        
        # Get current timestamp in readable format
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Log the query along with the timestamp
        print(f"[{timestamp}] [LOG] Executing SQL Query: {query}")
        
        # Call the original function
        return func(*args, **kwargs)
    return wrapper

# Function to fetch all users from the 'users' table in the database
@log_queries  # Apply the logging decorator
def fetch_all_users(query):
    # Connect to the SQLite database (creates 'users.db' if it doesn't exist)
    conn = sqlite3.connect('users.db')
    
    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()
    
    # Execute the provided SQL query
    cursor.execute(query)
    
    # Fetch all results from the executed query
    results = cursor.fetchall()
    
    # Close the connection to the database
    conn.close()
    
    # Return the fetched results
    return results

# Execute the function to fetch users, with logging of the SQL query and timestamp
users = fetch_all_users(query="SELECT * FROM users")

# Print the retrieved user data
print("Fetched Users:")
for user in users:
    print(user)
