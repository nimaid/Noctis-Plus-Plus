import os

from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QImage, QPixmap, QPainter, QColor

import constants

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


# Replaces all pixels with a specific color while still preserving transparency
def pixmap_alpha_colorfill(pixmap, color):
    output_pixmap = QPixmap(pixmap)
    
    painter = QPainter(output_pixmap)
    
    painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
    painter.fillRect(output_pixmap.rect(), QColor(color))
    painter.end()
    
    return output_pixmap


# Renders text with an image font QPixmap into an output QPixmap
def render_image_font(font_pixmap,
                      text,
                      align=constants.TextAlign.FLUSH_LEFT,
                      scale=1,
                      spacing=1,
                      color=None):
    if len(text) < 1:
        raise Exception("render_image_font() requires a non-zero length string as it's 'text'")
    if font_pixmap.width() % 128 != 0:
        raise Exception(f"render_image_font() requires a font image with a width divisible by 128. (input 'width': {font_pixmap.width()})")
    if scale % 1 != 0:
        raise TypeError(f"render_image_font() requires an integer as a scaling factor (input 'scale': {scale})")
    
    spacing = spacing * scale
    
    scaled_font_pixmap = font_pixmap.scaled(font_pixmap.width() * scale, font_pixmap.height() * scale, Qt.KeepAspectRatio, Qt.FastTransformation)
    if color != None:  # Only change the color if it's specified
        font_pixmap = pixmap_alpha_colorfill(scaled_font_pixmap, color)
    else:
        font_pixmap = scaled_font_pixmap
    
    char_width = font_pixmap.width() // 128
    char_height = font_pixmap.height()
    
    text_width = 0
    text_height = 0
    for line in text.split("\n"):
        line_width = len(line)
        
        if line_width > text_width:
            text_width = line_width
        
        text_height += 1
    
    width = (char_width * text_width) + (spacing * (text_width-1))
    height = (char_height * text_height) + (spacing * (text_height-1))
    
    pixmap = QPixmap(width, height)
    pixmap.fill(Qt.transparent)
    painter = QPainter(pixmap)
    
    for l, line in enumerate(text.split("\n")):
        line_width = (len(line) * (char_width + spacing)) - spacing
        line_blank_space = width - line_width
        
        x = 0
        y = l * (char_height + spacing)
        
        if align == constants.TextAlign.FLUSH_RIGHT:
            x += line_blank_space
        elif align == constants.TextAlign.CENTERED:
            x += line_blank_space // 2
        
        for c, char in enumerate(line):
            char_code = ord(char)
            if char_code not in range(0, 128):
                char_code = ord(" ")
            
            source_x = char_code * char_width
            source_y = 0

            source_rect = QRect(source_x, source_y, char_width, char_height)
            target_rect = QRect(x, y, char_width, char_height)

            painter.drawPixmap(target_rect, font_pixmap, source_rect)
            
            x += char_width + spacing
    
    return pixmap
