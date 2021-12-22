from fastapi import FastAPI

app = FastAPI()

@app.get("/habitat/")
async def root():
  return {"message": "alive"}

# any timer started
@app.post("/habitat/clockify/start")
async def timeIn():
  return {"message": "started"}

# any timer stopped
@app.post("/habitat/clockify/stop")
async def timeOut():
  return {"message": "stopped"}


@app.get("/habitat/location/{device}/{loc}")
async def location(device, loc):
  msg = "located {} {}".format(device, loc)
  print(msg)
  return {"message": msg}