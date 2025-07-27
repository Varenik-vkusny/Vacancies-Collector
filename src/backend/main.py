import logging
from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from .routers import jobs, keywords, users
from .database import async_engine, Base
from ..scheduler.jobs_and_users import run_main_parsing

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


async def db_init():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app = FastAPI()


app.include_router(jobs.router)
app.include_router(keywords.router)
app.include_router(users.router)

scheduler = AsyncIOScheduler(timezone = 'Asia/Almaty')

@app.on_event('startup')
async def startup():
    scheduler.add_job(run_main_parsing, trigger='interval', minutes=60)
    scheduler.start()
    logging.info('Планировщик запущен')
    await db_init()