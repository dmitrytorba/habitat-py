import os
from fastapi import FastAPI
from dotenv import load_dotenv
import requests

load_dotenv()

token = os.getenv('HUBITAT_API_TOKEN')
hubitatApi = os.getenv('HUBITAT_API_BASE')

app = FastAPI()
print("FastAPI started")


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
async def ring(device):
    msg = "ringing {}".format(device)
    print(msg)
    return {"message": msg}


@app.get("/habitat/battery-low/{device}")
async def lowBattery(device):
    msg = "low battery {}".format(device)
    print(msg)
    return {"message": msg}

officeMotion = False


@app.get("/habitat/office/motion/active")
async def officeMotionActive():
    global officeMotion
    officeMotion = True
    officeLights()
    print("officeMotionActive")
    return {"officeMotion": officeMotion}


@app.get("/habitat/office/motion/inactive")
async def officeMotionInactive():
    global officeMotion
    officeMotion = False
    officeLights()
    print("officeMotionActive")
    return {"officeMotion": officeMotion}

officeMotionId = 294

# prometheus node_exporter:
# node_power_supply_online

officeMonitorId = 625
officeCeilingSouthLightId = 65
officeCeilingNorthLightId = 630

p52IsActive = False

def officeLights():
    if p52IsActive or officeMotion:
        # requests.get(
        #     "{}{}/on?access_token={}".format(hubitatApi, officeMonitorId, token))
        requests.get("{}{}/on?access_token={}".format(hubitatApi,
                     officeCeilingSouthLightId, token))
        requests.get("{}{}/on?access_token={}".format(hubitatApi,
                     officeCeilingNorthLightId, token))
        print("officeLights on")

    if not p52IsActive and not officeMotion:
        # requests.get(
        #     "{}{}/off?access_token={}".format(hubitatApi, officeMonitorId, token))
        requests.get("{}{}/off?access_token={}".format(hubitatApi,
                     officeCeilingSouthLightId, token))
        requests.get("{}{}/off?access_token={}".format(hubitatApi,
                     officeCeilingNorthLightId, token))
        print("officeLights off")


@app.get("/habitat/p52/active")
async def p52Active():
    global p52IsActive
    p52IsActive = True
    officeLights()
    print("p52Active")
    return {"p52IsActive": p52IsActive}


@app.get("/habitat/p52/inactive")
async def p52Inactive():
    global p52IsActive
    p52IsActive = False
    officeLights()
    print("p52Inactive")
    return {"p52IsActive": p52IsActive}


@app.get("/habitat/office")
async def officeStatus():
    print("officeStatus")
    return {
        "officeMotion": officeMotion,
        "p52IsActive": p52IsActive
    }


async def getAllDevices():
    requests.get("{}/all?access_token={}".format(hubitatApi, token))
