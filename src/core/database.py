import asyncio
import os
import asyncpg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

async def create_pool():
  return await asyncpg.create_pool(DATABASE_URL, min_size=1, max_size=5)

async def test_pool():
  pool = await create_pool()
  test = await pool.fetchval("SELECT 1") 
  print(test)
  print("POOL CONNECTION TEST")
  await pool.close()

if __name__ == "__main__":
  asyncio.run(test_pool())