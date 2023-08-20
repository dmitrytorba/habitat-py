import requests
import json
import pandas as pd
from datetime import datetime, timedelta, date
from oura.v2 import OuraClientDataFrameV2
from dotenv import load_dotenv
import os

load_dotenv()


def fetch(url, params):
    headers = {"Authorization": "Bearer %s" % (os.getenv("OURA_TOKEN"))}
    response = requests.request("GET", url, headers=headers, params=params)

    if response.status_code != 200:
        print(response.text)
        return
    return response


def heartrate(start, end, filename):
    frame_end = end
    frame_start = frame_end - timedelta(days=29)
    df = pd.DataFrame()

    while start < frame_end:
        print("frame_start: ", frame_start)
        print("frame_end: ", frame_end)
        params = {"start_datetime": frame_start, "end_datetime": frame_end}
        response = fetch("https://api.ouraring.com/v2/usercollection/heartrate", params)
        json_object = json.loads(response.text)
        frame = pd.json_normalize(json_object["data"])
        df = pd.concat([df, frame])
        frame_end = frame_start
        frame_start = frame_end - timedelta(days=29)
        if start > frame_start:
            frame_start = start

    df.to_csv(filename)


def backup(start, end, filename, url):
    frame_end = end
    frame_start = frame_end - timedelta(days=29)
    df = pd.DataFrame()

    while start < frame_end:
        print("frame_start: ", frame_start)
        print("frame_end: ", frame_end)
        if isinstance(start, datetime):
            params = {"start_datetime": frame_start, "end_datetime": frame_end}
        else:
            params = {"start_date": frame_start, "end_date": frame_end}
        response = fetch(url, params)
        json_object = json.loads(response.text)
        frame = pd.json_normalize(json_object["data"])
        df = pd.concat([df, frame])
        frame_end = frame_start
        frame_start = frame_end - timedelta(days=29)
        if start > frame_start:
            frame_start = start

    df.to_csv(filename)


def lib_daily():
    v2 = OuraClientDataFrameV2(personal_access_token=token)

    # daily = v2.activity_df(start="2022-01-01", end="2022-04-01")
    heartrate = v2.heart_rate_df(start="2022-01-01", end="2023-01-01")
    heartrate.to_csv("heartrate.csv")


if __name__ == "__main__":
    # heartrate(datetime(2023, 1, 1), datetime.now(), "heartrate_2023.csv")
    # heartrate(datetime(2022, 1, 1), datetime(2022, 12, 31), "heartrate_2022.csv")

    backup(
        date(2023, 1, 1), date.today(), "activity_2023.csv", "https://api.ouraring.com/v2/usercollection/daily_activity"
    )
