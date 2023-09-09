from fastapi import FastAPI
from dotenv import load_dotenv
import discord_chat
from contextlib import asynccontextmanager
import scheduler
import asyncio
import logging

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
async def alive(lifespan=lifespan):
    return {"message": "OK"}
