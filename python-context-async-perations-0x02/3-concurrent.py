import aiosqlite
import asyncio

DB_NAME = 'users.db'

# Asynchronously fetch all users from the database
async def async_fetch_users():
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT * FROM users")
        results = await cursor.fetchall()
        await cursor.close()
        print("All Users:")
        for user in results:
            print(user)
        return results

# Asynchronously fetch users older than 40
async def async_fetch_older_users():
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT * FROM users WHERE age > ?", (40,))
        results = await cursor.fetchall()
        await cursor.close()
        print("\nUsers older than 40:")
        for user in results:
            print(user)
        return results

# Run both queries concurrently
async def fetch_concurrently():
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

# Kick off the concurrent execution
if __name__ == '__main__':
    asyncio.run(fetch_concurrently())


    """
    Requirements Recap:
Use aiosqlite (asynchronous SQLite client).

Create:

async_fetch_users()  fetches all users.

async_fetch_older_users() fetches users older than 40.

Use asyncio.gather() to run both concurrently.

Use asyncio.run(fetch_concurrently()) to kick it off.


What This Does:
async with aiosqlite.connect(...): asynchronously opens the connection.

await cursor.execute(...): executes queries without blocking the event loop.

asyncio.gather(...): runs both async functions concurrently.

asyncio.run(...): starts the event loop and runs fetch_concurrently().


    """