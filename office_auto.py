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

light_timeout = 5 * 60

last_active = None


def office_status():
    office_housekeeping(force=True)
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
    switch("office_ceiling_south", "on")
    switch("office_monitor", "on")
    switch("office_standing", "on")
    print("Lights on")


def lights_off():
    switch("office_ceiling_south", "off")
    switch("office_monitor", "off")
    switch("office_standing", "off")
    print("Lights off")


def office_housekeeping(force=False):
    global last_active
    print("Office housekeeping")
    if is_active() or force:
        last_active = time.time()
        print("force", force)
        print("Office is active")
        lights_on()
    else:
        if last_active is not None:
            elapsed = time.time() - last_active
            print("Office is not active, last active: {} {} {}".format(elapsed, time.time(), last_active))
            if elapsed > light_timeout:
                lights_off()
