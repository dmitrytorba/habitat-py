import os
from fastapi import FastAPI
from dotenv import load_dotenv
import requests

load_dotenv()

app = FastAPI()

@app.get("/habitat/")
async def root():
  return {"message": "alive"}

# any timer started
@app.post("/habitat/clockify/start")
async def timeIn():
  requests.get(os.getenv('HUBITAT_CLOCK_IN'))
  return {"message": "started"}

# any timer stopped
@app.post("/habitat/clockify/stop")
async def timeOut():
  requests.get(os.getenv('HUBITAT_CLOCK_OUT'))
  return {"message": "stopped"}


@app.get("/habitat/location/{device}/{loc}")
async def location(device, loc):
  msg = "located {} {}".format(device, loc)
  print(msg)
  return {"message": msg}


@app.get("/habitat/phone-ring/{device}")
async def location(device, loc):
  msg = "ringing {}".format(device)
  print(msg)
  return {"message": msg}


@app.get("/habitat/battery/{device}")
async def location(device, loc):
  msg = "ringing {}".format(device)
  print(msg)
  return {"message": msg}