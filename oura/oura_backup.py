import requests
import json
import pandas as pd
from datetime import datetime, timedelta, date
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


if __name__ == "__main__":
    backup(
        datetime(2023, 1, 1),
        datetime.now(),
        "heartrate_2023.csv",
        "https://api.ouraring.com/v2/usercollection/heartrate",
    )
    backup(
        datetime(2022, 1, 1),
        datetime(2022, 12, 31),
        "heartrate_2022.csv",
        "https://api.ouraring.com/v2/usercollection/heartrate",
    )

    backup(
        date(2023, 1, 1), date.today(), "activity_2023.csv", "https://api.ouraring.com/v2/usercollection/daily_activity"
    )

    backup(
        date(2022, 1, 1),
        date(2022, 12, 31),
        "activity_2022.csv",
        "https://api.ouraring.com/v2/usercollection/daily_activity",
    )

    backup(
        date(2023, 1, 1),
        date.today(),
        "readiness_2023.csv",
        "https://api.ouraring.com/v2/usercollection/daily_readiness",
    )

    backup(
        date(2022, 1, 1),
        date(2022, 12, 31),
        "readiness_2022.csv",
        "https://api.ouraring.com/v2/usercollection/daily_readiness",
    )

    backup(date(2023, 1, 1), date.today(), "sleep_2023.csv", "https://api.ouraring.com/v2/usercollection/daily_sleep")

    backup(
        date(2022, 1, 1),
        date(2022, 12, 31),
        "sleep_2022.csv",
        "https://api.ouraring.com/v2/usercollection/daily_sleep",
    )
