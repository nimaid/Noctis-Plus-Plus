import os

from PyQt5.QtGui import QImage, QPixmap

# General purpose text input stripper
def strip_all(input_text):
    return input_text.strip().strip("\n").strip("\r").strip()


# Makes sure a string represents a valid, existing file
# This can be used with argparse as a valid argument type
def file_path(string):
    if os.path.isfile(string):
        return string
    else:
        raise FileNotFoundError(string)


# Converts a PIl Image to a QPixmap
def image_to_pixmap(image):
    rgb_image = image.convert("RGB")
    qimage = QImage(
        rgb_image.tobytes(),
        rgb_image.width,
        rgb_image.height,
        3 * rgb_image.width,
        QImage.Format.Format_RGB888
    )
    pixmap = QPixmap.fromImage(qimage)

    return pixmap
