import schedule
import time
from unifi import block_tablets, unblock_tablets
import asyncio

schedule.every().day.at("07:00").do(unblock_tablets)
schedule.every().day.at("08:25").do(block_tablets)
schedule.every().day.at("12:30").do(unblock_tablets)
schedule.every().day.at("20:45").do(block_tablets)


async def main():
    print("Scheduler started")
    while True:
        n = schedule.idle_seconds()
        if n is None:
            # no more jobs
            break
        elif n > 0:
            # sleep exactly the right amount of time
            print(f"{n} seconds until next job, sleeping")
            await asyncio.sleep(n)
        schedule.run_pending()
