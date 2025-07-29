# Solution Steps

1. Identify that the endpoint /posts is making a database call without using 'await', which leads to a 500 error.

2. Ensure that asyncpg is used for asynchronous PostgreSQL queries, and the database query is awaited.

3. Define a Pydantic model (Post) to shape the returned posts in the API response.

4. Create a connection pool to the PostgreSQL database during FastAPI startup, using asyncpg.create_pool with the database URL.

5. On shutdown, close the database connection pool cleanly.

6. In the /posts endpoint function, acquire a connection from the pool asynchronously (with 'async with pool.acquire()'), then execute the SELECT query using 'await conn.fetch()'.

7. Convert the resulting rows (records) into a list of Post model instances.

8. Return the list of posts as the endpoint response.

9. Handle database or query errors by catching exceptions and raising a 500 HTTPException with a user-friendly error message.

