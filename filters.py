"""
Модуль фильтров для фоторедактора.
"""

import cv2


def apply_grayscale(image):
    """Применить фильтр оттенков серого."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)


def apply_blur(image, radius=5):
    """Применить фильтр размытия."""
    # Радиус Гауссова размытия должен быть нечетным числом
    if radius <= 0:
        return image
    kernel_size = radius * 2 + 1
    return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)


def apply_invert(image):
    """Инвертировать цвета."""
    return cv2.bitwise_not(image)


def apply_sharpen(image):
    """Увеличить резкость."""
    import numpy as np
    kernel_sharp = np.array([
        [-1, -1, -1],
        [-1, 9, -1],
        [-1, -1, -1]
    ])
    return cv2.filter2D(image, -1, kernel_sharp)