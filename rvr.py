import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import asyncio
from sphero_sdk import SpheroRvrAsync
from sphero_sdk import SerialAsyncDal
from sphero_sdk import RawMotorModesEnum
from pathlib import Path
import time


loop = asyncio.get_event_loop()

rvr = SpheroRvrAsync(
    dal=SerialAsyncDal(
        loop
        )
    )

speed = 75
rot_speed = 75


async def main():
    """ This program has RVR drive around in different directions.
    """

    await rvr.wake()

    await asyncio.sleep(2)

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

        print(teleop)
        if teleop == 'W':
            await rvr.raw_motors(
                left_mode=RawMotorModesEnum.forward.value,
                left_speed=speed,  # Valid speed values are 0-255
                right_mode=RawMotorModesEnum.forward.value,
                right_speed=speed  # Valid speed values are 0-255
                )

        elif teleop == 'S':
            await rvr.raw_motors(
                left_mode=RawMotorModesEnum.reverse.value,
                left_speed=speed,  # Valid speed values are 0-255
                right_mode=RawMotorModesEnum.reverse.value,
                right_speed=speed  # Valid speed values are 0-255
                )

        elif teleop == 'A':
            await rvr.raw_motors(
                left_mode=RawMotorModesEnum.reverse.value,
                left_speed=rot_speed,  # Valid speed values are 0-255
                right_mode=RawMotorModesEnum.forward.value,
                right_speed=rot_speed  # Valid speed values are 0-255
                )

        elif teleop == 'D':
            await rvr.raw_motors(
                left_mode=RawMotorModesEnum.forward.value,
                left_speed=rot_speed,  # Valid speed values are 0-255
                right_mode=RawMotorModesEnum.reverse.value,
                right_speed=rot_speed  # Valid speed values are 0-255
                )

        elif teleop == 'X':
            await rvr.raw_motors(
                left_mode=RawMotorModesEnum.forward.value,
                left_speed=0,  # Valid speed values are 0-255
                right_mode=RawMotorModesEnum.forward.value,
                right_speed=0  # Valid speed values are 0-255
                )
        else:
            continue

        await asyncio.sleep(0.5)

if __name__ == '__main__':
    try:
        loop.run_until_complete(
            main()
            )

    except KeyboardInterrupt:
        print('\nProgram terminated with keyboard interrupt.')

        loop.run_until_complete(
            rvr.close()
            )

    finally:
        if loop.is_running():
            loop.close()

