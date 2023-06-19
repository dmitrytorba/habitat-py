import os
from fastapi import FastAPI
from dotenv import load_dotenv
import requests
import logging

load_dotenv()

toly_internet = 640
mylo_pc_id = 558

office_monitor = 625
office_ceiling_south = 65
office_ceiling_north = 630

token = os.getenv("HUBITAT_API_TOKEN")
hubitat_api = "http://192.168.1.179/apps/api/611/devices/"


def mylo_pc(command):
    logging.info("mylo pc {}".format(command))
    requests.get("{}{}/{}?access_token={}".format(hubitat_api, mylo_pc_id, command, token))


if __name__ == "__main__":
    devices = requests.get("{}/all?access_token={}".format(hubitat_api, token))
    print(devices.json())
