import sys
import time
import _thread

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel
from PyQt5.QtGui import QPixmap, QImage, qRgb
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QPoint


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

    def __init__(self):
        super().__init__()
        self._screen_buffer = QImage(640, 480, QImage.Format_RGB16)

        self.resize(640, 480)
        self.setWindowTitle('Screen')
        self._w = QWidget()
        self._w.resize(640, 480)
        self.setCentralWidget(self._w)

        self._label = QLabel(self)
        self._label.setGeometry(0, 0, 640, 480)
        self._pixmap = QPixmap(640, 480)

        self._updater = VideoClock()
        self._updater.updated_screen_buffer.connect(self.update_screen)
        self._updater.start()


    def __del__(self):
        self._updater.stop()

    @pyqtSlot()
    def update_screen(self):
        self._label.setPixmap(QPixmap.fromImage(self._screen_buffer))
        self.repaint()


class TestVideo(QThread):
    def __init__(self, screen):
        super().__init__()
        self._screen = screen

    def __del__(self):
        self.wait()

    def run(self):
        time.sleep(1)
        for y in range(0,255):
            for x in range(0,255):
                self._screen._screen_buffer.setPixel(QPoint(x, y), qRgb(x, y, 255))
def main():
    app = QApplication(sys.argv)
    screen = ScreenEGA()
    screen.show()
    t = TestVideo(screen)
    t.start()


    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
