import sys
import time
import _thread

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel
from PyQt5.QtGui import QPixmap, QImage, qRgb
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QPoint


class PixelIndexError(Exception):
    def __init__(self):
        super().__init__()

class PixelColorError(Exception):
    def __init__(self):
        super().__init__()

class VideoClock(QThread):
    updated_screen_buffer = pyqtSignal()

    def __init__(self, cf=0.04):
        super().__init__()
        self._run = True
        self._clock_frequency = cf

    def __del__(self):
        self.wait()

    def run(self):
        while self._run:
            self.updated_screen_buffer.emit()
            time.sleep(self._clock_frequency)

    def stop(self):
        self._run = False


class ScreenEGA(QMainWindow):
    color_palette = [           # CGA color palette:
        qRgb(0, 0, 0),          # black             #000000
        qRgb(0, 0, 170),        # blue              #0000aa
        qRgb(0, 170, 0),        # green             #00aa00
        qRgb(0, 170, 170),      # cyan              #00aaaa
        qRgb(170, 0, 0),        # red               #aa0000
        qRgb(170, 0, 170),      # magenta           #aa00aa
        qRgb(170, 85, 0),       # brown             #aa5500
        qRgb(170, 170, 170),    # light grey        #aaaaaa
        qRgb(85, 85, 85),       # dark grey         #555555
        qRgb(85, 85, 255),      # bright blue       #5555ff
        qRgb(85, 255, 85),      # bright green      #55ff55
        qRgb(85, 255, 255),     # bright cyan       #55ffff
        qRgb(255, 85, 85),      # bright red        #ff5555
        qRgb(255, 85, 255),     # bright magenta    #ff55ff
        qRgb(255, 255, 85),     # bright yellow     #ffff55
        qRgb(255, 255, 255)     # bright white      #ffffff
    ]

    screen_width = 320
    screen_height = 200

    def __init__(self, scale=3):
        super().__init__()
        internal_dimension_x = ScreenEGA.screen_width*scale
        internal_dimension_y = ScreenEGA.screen_height*scale
        self._screen_scale = scale
        self._screen_buffer = QImage(internal_dimension_x, internal_dimension_y, QImage.Format_RGB16)

        self.resize(internal_dimension_x, internal_dimension_y)
        self.setWindowTitle('Screen')
        self._w = QWidget()
        self._w.resize(internal_dimension_x, internal_dimension_y)
        self.setCentralWidget(self._w)

        self._label = QLabel(self)
        self._label.setGeometry(0, 0, internal_dimension_x, internal_dimension_y)
        self._pixmap = QPixmap(internal_dimension_x, internal_dimension_y)

        self._updater = VideoClock()
        self._updater.updated_screen_buffer.connect(self.update_screen)
        self._updater.start()


    def __del__(self):
        self._updater.stop()

    @pyqtSlot()
    def update_screen(self):
        self._label.setPixmap(QPixmap.fromImage(self._screen_buffer))
        self.repaint()

    def setPixel(self, x, y, color_index):
        """ Set the pixel at the given position to the specified color
        Maps the virtual 320x200 screen to the actual 640x400 image

        :param x: x coordinate
        :param y: y coordinate
        :param color_index: index of the color in the CGA color palatte
        """
        if x >= 320 or x < 0:
            raise PixelIndexError()
        if y >= 200 or y < 0:
            raise PixelIndexError
        try:
            color = ScreenEGA.color_palette[color_index]
        except:
            raise PixelColorError()

        real_x = x*self._screen_scale
        real_y = y*self._screen_scale

        for _x in range(0, self._screen_scale):
            for _y in range(0, self._screen_scale):
                self._screen_buffer.setPixel(QPoint(real_x+_x, real_y+_y), color)



class TestVideo(QThread):
    def __init__(self, screen):
        super().__init__()
        self._screen = screen

    def __del__(self):
        self.wait()

    def run(self):
        color = 0
        for y in range(0,199):
            for x in range(0,319):
                self._screen.setPixel(x, y, color)
                if color >= 15:
                    color = 0
                else:
                    color = color + 1
def main():
    app = QApplication(sys.argv)
    screen = ScreenEGA(scale=3)
    screen.show()
    t = TestVideo(screen)
    t.start()


    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
