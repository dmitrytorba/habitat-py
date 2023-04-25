from fastapi import FastAPI
from dotenv import load_dotenv
import schedule
from unifi import block_tablets, unblock_tablets
import time

load_dotenv()

app = FastAPI()
print("FastAPI started")


@app.get("/alive")
async def alive():
    return {"message": "OK"}


schedule.every().day.at("07:00").do(unblock_tablets)
schedule.every().day.at("08:25").do(block_tablets)
schedule.every().day.at("12:30").do(unblock_tablets)
schedule.every().day.at("20:45").do(block_tablets)

while True:
    n = schedule.idle_seconds()
    if n is None:
        # no more jobs
        break
    elif n > 0:
        # sleep exactly the right amount of time
        print(f"{n} seconds until next job, sleeping")
        time.sleep(n)
    schedule.run_pending()
