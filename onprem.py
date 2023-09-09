from fastapi import FastAPI
from dotenv import load_dotenv
import discord_chat
from contextlib import asynccontextmanager
import scheduler
import asyncio
import logging
from office_auto import office_status

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("FastAPI started")
    logging.getLogger("asyncio").setLevel(logging.INFO)
    asyncio.create_task(discord_chat.main())
    asyncio.create_task(scheduler.main())
    yield
    print("FastAPI ended")


app = FastAPI(lifespan=lifespan)


@app.get("/alive")
async def alive():
    return {"message": "OK"}


@app.get("/office")
async def office():
    return office_status()
