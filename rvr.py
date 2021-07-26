import sys
import os
import time
from pathlib import Path

import asyncio

from sphero_sdk import SerialAsyncDal
from sphero_sdk import SpheroRvrAsync
from sphero_sdk import RawMotorModesEnum

# initialize global variables
speed = 75
rot_speed = 115

loop = asyncio.get_event_loop()
rvr = SpheroRvrAsync(
        dal=SerialAsyncDal(
            loop
            )
        )


async def main():
    global speed
    global heading
    global flags

    await rvr.wake()

    await rvr.reset_yaw()

    Path('teleop').touch()
    teleop_file = open('teleop', 'r')
    teleop_file.seek(0, os.SEEK_END)

    while True:
        line = teleop_file.readline()
        if not line:
            time.sleep(0.1)
            continue

        teleop = line.rstrip()

        if teleop == 'W':  # W
            print('W')
            await rvr.raw_motors(
                    left_mode=RawMotorModesEnum.forward.value,
                    left_duty_cycle=speed,  # Valid duty cycle range is 0-255
                    right_mode=RawMotorModesEnum.forward.value,
                    right_duty_cycle=speed  # Valid duty cycle range is 0-255
                    )
        elif teleop == 'A':  # A
            print('A')
            await rvr.raw_motors(
                    left_mode=RawMotorModesEnum.reverse.value,
                    left_duty_cycle=rot_speed,  # Valid duty cycle range is 0-255
                    right_mode=RawMotorModesEnum.forward.value,
                    right_duty_cycle=rot_speed  # Valid duty cycle range is 0-255
                    )
        elif teleop == 'S':  # S
            print('S')
            await rvr.raw_motors(
                    left_mode=RawMotorModesEnum.reverse.value,
                    left_duty_cycle=speed,  # Valid duty cycle range is 0-255
                    right_mode=RawMotorModesEnum.reverse.value,
                    right_duty_cycle=speed  # Valid duty cycle range is 0-255
                    )
        elif teleop == 'D':  # D
            print('D')
            await rvr.raw_motors(
                    left_mode=RawMotorModesEnum.forward.value,
                    left_duty_cycle=rot_speed,  # Valid duty cycle range is 0-255
                    right_mode=RawMotorModesEnum.reverse.value,
                    right_duty_cycle=rot_speed  # Valid duty cycle range is 0-255
                    )
        elif teleop == 'X':  # SPACE
            print('X')
            await rvr.raw_motors(
                    left_mode=RawMotorModesEnum.forward.value,
                    left_duty_cycle=0,  # Valid duty cycle range is 0-255
                    right_mode=RawMotorModesEnum.forward.value,
                    right_duty_cycle=0  # Valid duty cycle range is 0-255
                    )

        # sleep the infinite loop for a 10th of a second to avoid flooding the serial port.
        await asyncio.sleep(0.1)


def run_loop():
    global loop
    loop.run_until_complete( asyncio.gather(main()))


if __name__ == "__main__":
    try:
        run_loop()
    except KeyboardInterrupt:
        print("Keyboard Interrupt...")
    finally:
        print("Press any key to exit.")
        exit(1)
