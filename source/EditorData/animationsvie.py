from PyQt5.QtWidgets import QFileDialog, QPushButton
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap

class SlideshowWindow(QMainWindow):
    def __init__(self, filenames):
        super().__init__()
        
        self.image_index = 0
        self.filenames = filenames
        self.image_label = QLabel(self)
        self.setCentralWidget(self.image_label)

        self.show_image()

        self.timer = QTimer()
        self.timer.setInterval(500) # Задайте интервал таймера здесь
        self.timer.timeout.connect(self.show_image)
        self.timer.start()

        self.select_button = QPushButton('Select images', self)
        self.select_button.clicked.connect(self.select_images)
        self.select_button.move(20, 20)

    def select_images(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filenames, _ = QFileDialog.getOpenFileNames(self, "QFileDialog.getOpenFileNames()", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)", options=options)
        if filenames:
            self.filenames = filenames
            self.show_image()

    def show_image(self):
        filename = self.filenames[self.image_index]
        pixmap = QPixmap(filename)
        self.image_label.setPixmap(pixmap)
        self.image_index = (self.image_index + 1) % len(self.filenames)

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    # Замените список файлов на ваши собственные изображения.
    filenames = ['image1.png', 'image2.png', 'image3.png']

    window = SlideshowWindow(filenames)
    window.show()

    sys.exit(app.exec_())