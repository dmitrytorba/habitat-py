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


def office_status():
    return {
        "last_active": last_active,
    }


def p52_active():
    response = requests.get("https://sf8do.mooo.com/habitat/office")
    return response.json()["p52IsActive"]


def clockify_active():
    response = requests.get("https://sf8do.mooo.com/habitat/office")
    return response.json()["p52IsActive"]


def is_active():
    return p52_active() or is_motion("office_motion") or clockify_active()


def lights_on():
    switch("office_ceiling_south", "on")
    switch("office_monitor", "on")
    switch("office_standing", "on")


def lights_off():
    switch("office_ceiling_south", "off")
    switch("office_monitor", "off")
    switch("office_standing", "off")


def office_housekeeping():
    global last_active
    print("Office housekeeping")
    if is_active():
        last_active = time.time()
        print("Office is active")
    else:
        print("Office is not active, last active: {}".format(last_active))
