import numpy as np
from PIL import Image

def open_image(any_type_image : any) -> np.ndarray:
    image = Image.open(any_type_image)
    return np.array(image)
