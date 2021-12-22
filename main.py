from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "alive"}

# any timer started
@app.get("/clockify/start")
async def root():
    return {"message": "started"}

# any timer stopped
@app.get("/clockify/stop")
async def root():
    return {"message": "stopped"}
