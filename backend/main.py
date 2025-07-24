from fastapi import FastAPI
from .routers import jobs, keywords, users
from .database import async_engine, Base


async def db_init():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app = FastAPI()


app.include_router(jobs.router)
app.include_router(keywords.router)
app.include_router(users.router)

@app.on_event('startup')
async def startup():
    await db_init()