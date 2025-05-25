from fastapi import FastAPI
from app.database import engine, Base
from app.routers import users

app = FastAPI()

@app.on_event('startup')
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(users.router)

@app.get('/')
def read_root():
    return {'message': 'Library API'}