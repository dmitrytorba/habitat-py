import schedule
import time
from unifi import block_tablets, unblock_tablets
import asyncio
import discord_chat
import asyncio
import logging
from hubitat import mylo_pc
from office_auto import office_housekeeping


def mylo_sleep_warning():
    logging.info("mylo_sleep_warning")
    asyncio.create_task(
        discord_chat.send_message(
            "Time to RELAX and get ready for SLEEP, Mylo!! I will terminate your computer in 5 minutes."
        )
    )


def mylo_sleep_off():
    mylo_pc("off")
    asyncio.create_task(discord_chat.send_message("Hasta la vista, Mylo PC is now terminated."))


def five_minutes():
    print("Five minutes")
    office_housekeeping()


schedule.every().day.at("12:00").do(unblock_tablets)
schedule.every().day.at("20:45").do(block_tablets)
schedule.every().day.at("21:10").do(mylo_sleep_warning)
schedule.every().day.at("21:15").do(mylo_sleep_off)
schedule.every(1).minutes.do(five_minutes)


async def main():
    # logger does not work here
    print("Scheduler started")
    while True:
        n = schedule.idle_seconds()
        if n is None:
            # no more jobs
            break
        elif n > 5:
            # sleep exactly the right amount of time
            print(f"{n} seconds until next job, sleeping")
            await asyncio.sleep(n)
        print("Running pending jobs")
        schedule.run_pending()
