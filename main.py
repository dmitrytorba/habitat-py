from fastapi import FastAPI

app = FastAPI()


@app.get("/habitat/")
async def root():
    return {"message": "alive"}

# any timer started
@app.get("/habitat/clockify/start")
async def root():
    return {"message": "started"}

# any timer stopped
@app.get("/habitat/clockify/stop")
async def root():
    return {"message": "stopped"}
