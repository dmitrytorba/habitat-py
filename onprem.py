from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
print("FastAPI started")


@app.get("/alive")
async def alive():
    return {"message": "OK"}
