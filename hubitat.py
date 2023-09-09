import os
from fastapi import FastAPI
from dotenv import load_dotenv
import requests
import logging

load_dotenv()

hubitat_ids = {
    "toly_internet": 640,
    "mylo_pc": 558,
    "office_monitor": 625,
    "office_ceiling_south": 65,
    "office_motion": 294,
    "office_standing": 456,
}

token = os.getenv("HUBITAT_API_TOKEN")
hubitat_api = "http://192.168.1.179/apps/api/611/devices/"


def mylo_pc(command):
    logging.info("mylo pc {}".format(command))
    requests.get("{}{}/{}?access_token={}".format(hubitat_api, hubitat_ids["mylo_pc"], command, token))


def switch(device, command):
    logging.info("switch {} {}".format(device, command))
    device_id = hubitat_ids[device]
    requests.get("{}{}/{}?access_token={}".format(hubitat_api, device_id, command, token))


def get_attribute(device, attribute):
    device_id = hubitat_ids[device]
    response = requests.get("{}{}?access_token={}".format(hubitat_api, device_id, token))
    if response.status_code != 200:
        logging.error(response.text)
        return None
    attributes = response.json()["attributes"]
    for attribute in attributes:
        if attribute["name"] == attribute:
            return attribute["currentValue"]
    return None


def is_motion(device):
    return get_attribute(device, "motion") == "active"


if __name__ == "__main__":
    devices = requests.get("{}/all?access_token={}".format(hubitat_api, token))
    print(devices.json())
