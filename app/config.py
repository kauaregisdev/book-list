import os

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql+asyncpg://admin:admin123@localhost:5000/library')