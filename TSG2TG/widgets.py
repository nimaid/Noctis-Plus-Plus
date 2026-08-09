import math
from PyQt5.QtCore import Qt, QRect, QPoint, QRectF, QSize, pyqtSignal
from PyQt5.QtWidgets import (
    QAbstractButton, QSlider, QStyle, QLabel, QWidget,
    QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QFrame
)
from PyQt5.QtGui import QBrush, QColor, QPixmap, QPainter


# Custom image-based button
#   Allows for very fancy custom buttons
class ImageButton(QAbstractButton):
    def __init__(self,
                 pixmap,
                 pixmap_hover,
                 pixmap_pressed,
                 scale=1.0,
                 parent=None
                 ):
        super(ImageButton, self).__init__(parent)
        self.scale = scale
        self.height = None
        self.width = None
        self.pixmap_pressed = None
        self.pixmap_hover = None
        self.pixmap = None

        self.change_pixmaps(
            pixmap=pixmap,
            pixmap_hover=pixmap_hover,
            pixmap_pressed=pixmap_pressed
        )

        self.pressed.connect(self.update)
        self.released.connect(self.update)

    def change_pixmaps(self,
                       pixmap,
                       pixmap_hover,
                       pixmap_pressed
                       ):
        self.pixmap = pixmap
        self.pixmap_hover = pixmap_hover
        self.pixmap_pressed = pixmap_pressed

        self.width = round(self.pixmap.width() * self.scale)
        self.height = round(self.pixmap.height() * self.scale)

        self.update()

    def paintEvent(self, event):
        if self.isDown():
            pix = self.pixmap_pressed
        elif self.underMouse():
            pix = self.pixmap_hover
        else:
            pix = self.pixmap

        painter = QPainter(self)
        painter.drawPixmap(event.rect(), pix)

    def enterEvent(self, event):
        self.update()

    def leaveEvent(self, event):
        self.update()

    def sizeHint(self):
        return QSize(self.width, self.height)


# Custom image-based label
#   Allows for very fancy custom labels
class ImageLabel(QLabel):
    def __init__(self,
                 pixmap,
                 scale=1.0,
                 parent=None
                 ):
        super(ImageLabel, self).__init__(parent)
        self.pixmap = pixmap
        self.scale = scale

        self.width = round(self.pixmap.width() * self.scale)
        self.height = round(self.pixmap.height() * self.scale)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(event.rect(), self.pixmap)

    def sizeHint(self):
        return QSize(self.width, self.height)


# Custom image-based font widget
#   Allows for custom image-based fonts
class ImageFont(QWidget):
    def __init__(self,
               font_pixmap,
               scale=1,
               spacing=1,
               default_text=None
               ):
        super(ImageFont, self).__init__()
        if scale % 1 != 0:
                raise TypeError("ImageFont requires an integer as a scaling factor")
        self.scale = scale
        self.spacing = spacing * self.scale
        
        self.font_pixmap = font_pixmap.scaled(font_pixmap.width() * self.scale, font_pixmap.height() * self.scale, Qt.KeepAspectRatio, Qt.FastTransformation)
        
        if font_pixmap.width() % 128 != 0:
            raise Exception(f"ImageFont requires a font image with a width divisible by 128. (input width: {font_pixmap.width()})")
        self.char_width = self.font_pixmap.width() // 128
        self.char_height = self.font_pixmap.height()
        
        if default_text != None:
            self.set_text(default_text)
    
    def set_text(self, text):
        self.text = text
        
        text_length = len(self.text)
        self.setFixedSize((self.char_width * text_length) + (self.spacing * (text_length-1)), self.char_height)
        
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        x = event.rect().x()
        y = event.rect().y()

        for i, char in enumerate(self.text):
            source_x = ord(char) * self.char_width
            source_y = 0

            source_rect = QRect(source_x, source_y, self.char_width, self.char_height)
            target_rect = QRect(x, y, self.char_width, self.char_height)

            painter.drawPixmap(target_rect, self.font_pixmap, source_rect)
            
            x += self.char_width
            
            if i < len(self.text) - 1:
                x += self.spacing


# Custom seekbar class
#   A customized slider
class SeekBar(QSlider):
    def __init__(self,
                 parent=None,
                 position_changed_callback=None,
                 handle_size=10,
                 color="#666",
                 hover_color="#000"
                 ):
        super(SeekBar, self).__init__(parent)

        self.handle_size = handle_size
        # TODO: Fix handle width not changing
        # TODO: Fix handle not hanging over the side

        self.setFixedHeight(self.handle_size)

        self.setStyleSheet(
            "QSlider::handle {{ background: {2}; height: {0}px; width: {0}px; border-radius: {1}px; }} "
            "QSlider::handle:hover {{ background: {3}; height: {0}px; width: {0}px; border-radius: {1}px; }}".format(
                self.handle_size,
                math.floor(self.handle_size / 2),
                color,
                hover_color
            )
        )

        self.position_changed_callback = position_changed_callback

    def set_position(self, value, do_callback=True):
        if self.position_changed_callback is not None and do_callback:
            self.position_changed_callback(value)

        self.setValue(value)

    def mousePressEvent(self, event):
        value = QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), event.x(), self.width())
        self.set_position(value)

    def mouseMoveEvent(self, event):
        value = QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), event.x(), self.width())
        self.set_position(value)


# Custom interactive graphics view class
#   A widget that allows user interaction like panning and zooming with the mouse
class PhotoViewer(QGraphicsView):
    photoClicked = pyqtSignal(QPoint)

    def __init__(self, parent, background=QColor(30, 30, 30)):
        super(PhotoViewer, self).__init__(parent)

        self._zoom = 0
        self._empty = True

        self._scene = QGraphicsScene(self)
        self._photo = QGraphicsPixmapItem()

        self._scene.addItem(self._photo)
        self.setScene(self._scene)

        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setBackgroundBrush(QBrush(background))
        self.setFrameShape(QFrame.NoFrame)

        self.setRenderHints(QPainter.Antialiasing)

    def has_photo(self):
        return not self._empty

    def set_photo(self, pixmap=None):
        self._zoom = 0
        if pixmap and not pixmap.isNull():
            self._empty = False
            self.setDragMode(QGraphicsView.ScrollHandDrag)
            self._photo.setPixmap(pixmap)
        else:
            self._empty = True
            self.setDragMode(QGraphicsView.NoDrag)
            self._photo.setPixmap(QPixmap())
        self.fitInView()

    def fitInView(self, scale=True, **kwargs):
        rect = QRectF(self._photo.pixmap().rect())
        if not rect.isNull():
            self.setSceneRect(rect)
            if self.has_photo():
                unity = self.transform().mapRect(QRectF(0, 0, 1, 1))
                self.scale(1 / unity.width(), 1 / unity.height())
                view_rect = self.viewport().rect()
                scene_rect = self.transform().mapRect(rect)
                factor = min(view_rect.width() / scene_rect.width(),
                             view_rect.height() / scene_rect.height())
                self.scale(factor, factor)
            self._zoom = 0

    def wheelEvent(self, event):
        if self.has_photo():
            if event.angleDelta().y() > 0:
                factor = 1.25
                self._zoom += 1
            else:
                factor = 0.8
                self._zoom -= 1
            if self._zoom > 0:
                self.scale(factor, factor)
            elif self._zoom == 0:
                self.fitInView()
            else:
                self._zoom = 0
