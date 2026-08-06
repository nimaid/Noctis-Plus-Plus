import math
from PyQt5.QtCore import Qt, QPoint, QRectF, pyqtSignal
from PyQt5.QtWidgets import (
    QSlider, QStyle,
    QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QFrame
)
from PyQt5.QtGui import QBrush, QColor, QPixmap, QPainter


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
