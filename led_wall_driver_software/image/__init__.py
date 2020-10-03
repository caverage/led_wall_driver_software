"""convert an image to the rgb values for fastled"""

from pathlib import Path

import numpy as np  # type:ignore
from PIL import Image  # type:ignore


def _image_to_array(image: Path) -> np.ndarray:
    """ Turn an image into a Numpy Array

    Args:
        image: the image to be turned into an array

    Returns:
        np.ndarray: the an array from the image
    """
    return np.asarray(Image.open(image))
