from typing import Union, Iterable
import numpy as np


class PyghthouseCanvas:

    VALID_IMAGE_TYPE = Union[np.ndarray, Iterable, int]
    IMAGE_SHAPE = (14, 28, 3)

    def __init__(self, initial_image=None):
        self.image = np.zeros(self.IMAGE_SHAPE, dtype=np.ubyte)
        if initial_image is None:
            self.image[:, :, 0] = 255
        else:
            self.set_image(initial_image)

    def set_image(self, new_image: VALID_IMAGE_TYPE) -> np.array:
        try:
            self.image[:] = np.asarray(new_image).reshape(self.IMAGE_SHAPE)
        except ValueError as e:
            raise ValueError(f"{e}. Most likely, your image does not have the correct dimensions.") from None

        return self.image

    def get_image_bytes(self):
        return self.image.tobytes()
