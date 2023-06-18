import schedule
import time
from unifi import block_tablets, unblock_tablets
import asyncio
import discord_chat
import asyncio
import logging

schedule.every().day.at("07:00").do(unblock_tablets)
schedule.every().day.at("08:25").do(block_tablets)
schedule.every().day.at("12:30").do(unblock_tablets)
schedule.every().day.at("20:45").do(block_tablets)


def mylo_sleep_warning():
    logging.info("mylo_sleep_warning")
    asyncio.create_task(
        discord_chat.send_message(
            "Time to RELAX and get ready for SLEEP, Mylo!! I will terminate your computer in 5 minutes."
        )
    )


schedule.every().day.at("20:40").do(mylo_sleep_warning)


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
