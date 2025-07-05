import seed  # Import your database utility module

def paginate_users(page_size, offset):
    """
    Fetch a single page of users from the database.
    Returns a list of rows (dictionaries) using LIMIT and OFFSET.
    """
    connection = seed.connect_to_prodev()  # Connect to ALX_prodev database
    cursor = connection.cursor(dictionary=True)  # Use dictionary cursor for readable keys
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()  # Fetch all rows from this page
    cursor.close()
    connection.close()
    return rows  # Return list of user rows


def lazy_pagination(page_size):
    """
    Generator that yields user data pages lazily, one page at a time.
    It fetches new pages from the database only when needed.
    """
    offset = 0  # Start from the first record
    while True:
        page = paginate_users(page_size, offset)  # Fetch a batch of users
        if not page:
            break  # Stop when no more data is returned
        yield page  # Yield the current page
        offset += page_size  # Move the offset forward for the next page

# Test block (optional, for debugging only)
if __name__ == "__main__":
    for page in lazy_pagination(10):
        for user in page:
            print(user)
