import os
from fastapi import FastAPI
from dotenv import load_dotenv
import requests

load_dotenv()

p52_active = False
clockify_active = False

token = os.getenv("HUBITAT_API_TOKEN")
hubitatApi = os.getenv("HUBITAT_API_BASE")

app = FastAPI()
print("FastAPI started")


@app.get("/habitat/")
async def root():
    return {"message": "alive"}


# any timer started
@app.post("/habitat/clockify/start")
async def timeIn():
    global clockify_running
    clockify_running = True
    requests.get(os.getenv("HUBITAT_CLOCK_IN"))
    return {"message": "started"}


# any timer stopped
@app.post("/habitat/clockify/stop")
async def timeOut():
    global clockify_running
    clockify_running = False
    requests.get(os.getenv("HUBITAT_CLOCK_OUT"))
    return {"message": "stopped"}


@app.get("/habitat/location/{device}/{loc}")
async def location(device, loc):
    msg = "located {} {}".format(device, loc)
    print(msg)
    return {"message": msg}


@app.get("/habitat/phone-ring/{device}")
async def ring(device):
    msg = "ringing {}".format(device)
    print(msg)
    return {"message": msg}


@app.get("/habitat/battery-low/{device}")
async def lowBattery(device):
    msg = "low battery {}".format(device)
    print(msg)
    return {"message": msg}


async def getAllDevices():
    requests.get("{}/all?access_token={}".format(hubitatApi, token))


@app.get("/habitat/p52/active")
async def p52Active():
    global p52_active
    p52_active = True
    return {"p52_active": p52_active}


@app.get("/habitat/p52/inactive")
async def p52Inactive():
    global p52_active
    p52_active = False
    return {"p52_active": p52_active}


@app.get("/habitat/office")
async def officeStatus():
    return {"p52_active": p52_active, "clockify_active": clockify_active}
