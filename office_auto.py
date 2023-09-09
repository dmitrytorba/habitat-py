import os
from fastapi import FastAPI
from dotenv import load_dotenv
import requests
from hubitat import switch, is_motion
import logging
import time


load_dotenv()

# prometheus node_exporter:
# node_power_supply_online

last_active = None
lights_activated = False


def office_status():
    return {
        "last_active": last_active,
    }


def get_cloud_status():
    response = requests.get("https://sf8do.mooo.com/habitat/office")
    return response.json()


def is_active():
    cloud_status = get_cloud_status()
    office_motion = is_motion("office_motion")
    print("cloud_status", cloud_status)
    print("office_motion", office_motion)
    return cloud_status["p52_active"] or cloud_status["clockify_active"] or office_motion


def lights_on():
    global lights_activated
    lights_activated = True
    switch("office_ceiling_south", "on")
    switch("office_monitor", "on")
    switch("office_standing", "on")


def lights_off():
    global lights_activated
    lights_activated = False
    switch("office_ceiling_south", "off")
    switch("office_monitor", "off")
    switch("office_standing", "off")


def office_housekeeping():
    global last_active
    print("Office housekeeping")
    if is_active():
        last_active = time.time()
        print("Office is active")
        if not lights_activated:
            lights_on()
    else:
        elapsed = time.time() - last_active
        print("Office is not active, last active: {}".format(elapsed))
        if lights_activated and elapsed > 30 * 60:
            lights_off()
