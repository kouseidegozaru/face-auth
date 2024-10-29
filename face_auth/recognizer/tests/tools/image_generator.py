import numpy as np

def generate_random_image() -> np.ndarray:
    image = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
    return image