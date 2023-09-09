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


def p52_status():
    response = requests.get("https://sf8do.mooo.com/habitat/office")
    return response.json()["p52IsActive"]


def is_active():
    return p52_status() and is_motion("office_motion")


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
    logging.info("Office housekeeping")
    if is_active():
        last_active = time.time()
        logging.info("Office is active")
    else:
        logging.info("Office is not active, last active: {}".format(last_active))
