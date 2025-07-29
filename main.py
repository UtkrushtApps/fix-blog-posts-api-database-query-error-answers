from fastapi import FastAPI, HTTPException
from typing import List
from pydantic import BaseModel
import asyncpg
import os

app = FastAPI()

# Example Post model (simplified)
class Post(BaseModel):
    id: int
    title: str
    content: str

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/blogdb")

# Global database connection pool
pool = None

@app.on_event("startup")
async def startup():
    global pool
    pool = await asyncpg.create_pool(DATABASE_URL)

@app.on_event("shutdown")
async def shutdown():
    global pool
    if pool:
        await pool.close()

@app.get("/posts", response_model=List[Post])
async def get_posts():
    global pool
    try:
        async with pool.acquire() as conn:
            rows = await conn.fetch("SELECT id, title, content FROM posts")
            posts = [Post(id=row['id'], title=row['title'], content=row['content']) for row in rows]
            return posts
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch posts")
