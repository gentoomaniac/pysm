import sys
import time

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel
from PyQt5.QtGui import QPixmap, QImage, qRgb
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QPoint

from characters import ascii_dos

class PixelIndexError(Exception):
    def __init__(self):
        super().__init__()

class PixelColorError(Exception):
    def __init__(self):
        super().__init__()

class CharacterIndexError(Exception):
    def __init__(self):
        super().__init__()

class AsciiIndexError(Exception):
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

    character_cell_width = 8
    character_cell_height = 8

    def __init__(self, scale=3):
        super().__init__()
        internal_dimension_x = ScreenEGA.screen_width*scale
        internal_dimension_y = ScreenEGA.screen_height*scale
        self._screen_scale = scale
        self._screen_buffer = QImage(internal_dimension_x, internal_dimension_y, QImage.Format_RGB16)
        self.cls()

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

    def cls(self):
        self._screen_buffer.fill(ScreenEGA.color_palette[0])

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

    def setCharacter(self, c, x, y, color):
        if c < 0 or c > 254:
            raise AsciiIndexError()
        if x < 0 or x >= ScreenEGA.screen_width/ScreenEGA.character_cell_width:
            raise CharacterIndexError()
        if y < 0 or y >= ScreenEGA.screen_height/ScreenEGA.character_cell_height:
            raise CharacterIndexError()

        real_x = x*ScreenEGA.character_cell_width
        real_y = y*ScreenEGA.character_cell_height

        for xp in range(0, ScreenEGA.character_cell_width):
            for yp in range(0, ScreenEGA.character_cell_height):
                if ascii_dos[c][yp][xp]:
                    self.setPixel(real_x+xp, real_y+yp, color)

    def drawLine(self, a, b, color):
        # special case: vertical line
        if a[0] == b[0]:
            if a[1] < b[1]:
                x1, y1 = a
                x2, y2 = b
            else:
                x1, y1 = b
                x2, y2 = a

            for xi in range(y1, y2):
                self.setPixel(x1, xi, color)
            return


        if a[0] < b[0]:
            x1, y1 = a
            x2, y2 = b
        else:
            x1, y1 = b
            x2, y2 = a

        slope = round((y2 - y1) / (x2 - x1), 2)   # slope per pixel
        print(slope)

        x_current, y_current = x1, y1
        for xi in range(x1, x2):
            print(xi)
            y_new = y_current + slope
            if slope <= 1 and slope >= -1:
                try:
                    self.setPixel(xi, round(y_new), color)
                except PixelIndexError:
                    continue
            else:

                for yi in range(round(y_current), round(y_current+abs(slope))):
                    try:
                        self.setPixel(xi, round(yi), color)
                    except PixelIndexError:
                        continue

            x_current, y_current = xi, y_new


class TestVideo(QThread):
    def __init__(self, screen):
        super().__init__()
        self._screen = screen

    def __del__(self):
        self.wait()

    def run(self):
        #color = 0
        #for y in range(0,199):
        #    for x in range(0,319):
        #        self._screen.setPixel(x, y, color)
        #        if color >= 15:
        #            color = 0
        #        else:
        #            color = color + 1

        #c = 1
        #for x in range(0,40):
        #    for y in range(0,25):
        #        self._screen.setCharacter(c, x, y, 10)
        #        c = 1 if c == 2 else 2

        #c = 0
        #color = 1
        #for y in range(0, 25):
        #    for x in range(0, 40):
        ##        self._screen.cls()
        #        self._screen.setCharacter(c, x, y, color)
        #        c = 0 if c >= len(ascii_dos)-1 else c+1
        #        color = 1 if color >= 15 else color+1
        ##        time.sleep(0.5)

        self._screen.drawLine((10, 10), (100, 30), 5)
        self._screen.drawLine((20, 20), (20, 100), 6)
        self._screen.drawLine((30, 30), (35, 50), 7)
        self._screen.drawLine((70, 120), (65, 199), 8)


def main():
    app = QApplication(sys.argv)
    screen = ScreenEGA(scale=4)
    screen.show()
    t = TestVideo(screen)
    t.start()


    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
