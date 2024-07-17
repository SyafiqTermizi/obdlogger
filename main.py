import logging
import os
import time

import obd
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


def get_connection():
    port = os.environ.get("OBD_PORT", "")
    baud = os.environ.get("OBD_BAUD_RATE", "")

    logger.info(f"Using parameter {port} {baud}")

    return obd.Async(
        portstr=port,
        baudrate=baud,
    )


def log_temp(val):
    with open("log_temp.log", "a") as log:
        log.write(f"{time.time()}, {val.value}\n")


def log_rpm(val):
    with open("log_rpm.log", "a") as log:
        log.write(f"{time.time()}, {val.value}\n")


def log_speed(val):
    with open("log_speed.log", "a") as log:
        log.write(f"{time.time()}, {val.value}\n")


def log_throttle(val):
    with open("log_throttle.log", "a") as log:
        log.write(f"{time.time()}, {val.value}\n")


if __name__ == "__main__":
    load_dotenv()

    logger.info("Initializing connection...")
    connection = get_connection()
    logger.info("Connected to OBD 2!")

    connection.watch(obd.commands.COOLANT_TEMP)
    connection.watch(obd.commands.RPM)
    connection.watch(obd.commands.SPEED)
    connection.watch(obd.commands.THROTTLE_POS)

    try:
        connection.start()
    except KeyboardInterrupt:
        connection.stop()
        connection.unwatch_all()
