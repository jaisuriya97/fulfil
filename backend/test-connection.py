import os
import psycopg2
import redis
from dotenv import load_dotenv

load_dotenv()

print("--- Testing Database and Redis Connections ---")

db_url = os.getenv('DATABASE_URL')
if not db_url:
    print("PostgreSQL: FAILED (DATABASE_URL not found in .env)")
else:
    try:
        conn = psycopg2.connect(db_url)
        print("PostgreSQL: Connection successful!")
        conn.close()
    except Exception as e:
        print(f"PostgreSQL: FAILED. Error: {e}")

redis_url = os.getenv('REDIS_URL')
if not redis_url:
    print("Redis: FAILED (REDIS_URL not found in .env)")
else:
    try:
        r = redis.from_url(redis_url, socket_connect_timeout=5)
        r.ping()
        print("Redis: Connection successful!")
    except Exception as e:
        print(f"Redis: FAILED. Error: {e}")

print("--- Test Complete ---")