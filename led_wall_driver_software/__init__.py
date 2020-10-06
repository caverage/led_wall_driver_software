""" Drive a Matrix of LED's using a microcontroller.

This relies on a microcontroller that is flashed with specific firmware."""
import time
from pathlib import Path
from typing import Any

import numpy as np  # type:ignore
import serial  # type:ignore
from nptyping import NDArray, UInt8  # type:ignore


class LEDWall:
    def __init__(
        self,
        led_wall_port: serial.Serial,
        width: int,
        height: int,
        serpentine: bool = True,
    ):
        self.led_wall_port = led_wall_port

        self.width = width
        self.height = height
        self._frame_type = NDArray[(self.width, self.height, 3), UInt8]

        self.serpentine = serpentine

    # FIXME: https://github.com/ramonhagenaars/nptyping/issues/37
    def __call__(self, frame: NDArray[(Any, Any, 3), UInt8]) -> None:
        # if (
        #     not frame.shape == (self.width, self.height, 3)
        #     or not frame.dtype == np.uint8
        # ):
        #     raise RuntimeError(
        #         "Incorrect frame dimensions: Expected: "
        #         f"({self.width}, {self.height}, 3) "
        #         f"Got: {frame.shape}"
        #     )

        if self.serpentine:
            frame = self._serpentinize(frame)

        self.led_wall_port.write(frame.tobytes())

        # wait for the LED wall to respond
        self.led_wall_port.readline()

    # FIXME: https://github.com/ramonhagenaars/nptyping/issues/37
    @staticmethod
    def _serpentinize(
        input_array: NDArray[(Any, Any, 3), UInt8]
    ) -> NDArray[(Any, Any, 3), UInt8]:
        """ Serpentinize input array

        See also: boustrophedon

        Args:
            input_array: array to serpentinize

        Returns:
            NDArray[(Any, Any, 3), UInt8]
        """

        input_array[1::2] = input_array[1::2, ::-1]
        return input_array
