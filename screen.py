import sys
import time
import _thread

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot


class Updater(QThread):
    updated_screen_buffer = pyqtSignal()

    def __init__(self):
        super().__init__()

    def __del__(self):
        self.wait()

    def run(self):
        for i in range(1, 10):
            print(i)
            self.updated_screen_buffer.emit()
            time.sleep(1)


class ScreenVGA(QMainWindow):

    def __init__(self):
        super().__init__()
        self.resize(640, 480)
        self.setWindowTitle('Screen')
        self._w = QWidget()
        self._w.resize(640, 480)
        self.setCentralWidget(self._w)

        self._label = QLabel(self)
        self._label.setGeometry(0, 0, 640, 480)
        self._pixmap = QPixmap(640, 480)
        self.show()

        self._updater = Updater()
        self._updater.updated_screen_buffer.connect(self.update_screen)
        self._updater.start()

    def __del__(self):
        self._updater.exit()

    @pyqtSlot()
    def update_screen(self):
        self._label.setPixmap(self._pixmap)
        self.repaint()


def main():
    app = QApplication(sys.argv)
    screen = ScreenVGA()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
