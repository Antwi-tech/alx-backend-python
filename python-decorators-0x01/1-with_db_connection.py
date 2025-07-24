import sqlite3 
import functools

'''

def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')  # Open connection
        try:
            result = func(conn, *args, **kwargs)  # Pass connection to the function
            return result
        finally:
            conn.close()  # Ensure connection is closed even if an error occurs
    return wrapper

@with_db_connection 
def get_user_by_id(conn, user_id): 
    cursor = conn.cursor() 
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,)) 
    return cursor.fetchone() 

# Fetch user by ID with automatic connection handling 
user = get_user_by_id(user_id=2)
print(user)

'''

def another(func):
    def wrapper(*args ):
       my_name = args[0]
       print(f"You said your name is {my_name}")
       func(*args )
    return wrapper

@another
def usr_name(name):
    print(f"My name is {name}")
    
usr_name("Antwiwaa")  