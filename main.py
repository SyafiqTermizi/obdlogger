import os
import time

import obd
from dotenv import load_dotenv


def get_connection():
    return obd.Async(
        portstr=os.environ.get("OBD_PORT", ""),
        baudrate=os.environ.get("OBD_BAUD_RATE", ""),
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

    connection = get_connection()
    connection.watch(obd.commands.COOLANT_TEMP)
    connection.watch(obd.commands.RPM)
    connection.watch(obd.commands.SPEED)
    connection.watch(obd.commands.THROTTLE_POS)

    try:
        connection.start()  # start the async update loop
    except KeyboardInterrupt:
        connection.stop()
        connection.unwatch_all()
