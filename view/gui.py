from PySide6 import QtWidgets
from PySide6 import QtGui
from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtCore import Qt


from model.data import Data

from pathlib import Path
from typing import Callable, Iterator
from contextlib import contextmanager
import sys


@contextmanager
def init_app() -> Iterator:
    """
    Context manager to safely exit the app.
    """
    app = QApplication(sys.argv)
    yield app
    sys.exit(app.exec_())


class Window(QMainWindow):
    def __init__(
        self,
        data: Data,
        stylesheet: str,
        create_hist_fn: Callable[[Data], None],
        save_data_fn: Callable[[Data], None],
    ) -> None:
        super().__init__()

        self.data = data
        self.create_hist_fn = create_hist_fn
        self.save_data_fn = save_data_fn

        self.win_width = 800
        self.win_height = 700
        self.title = "Histogram Maker"
        self.spacing_left = 200
        self.spacing_top = 200

        self.init_ui()
        self.setStyleSheet(stylesheet)

    def init_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(
            self.spacing_left,
            self.spacing_top,
            self.win_width,
            self.win_height,
        )

        self.label_file = QtWidgets.QLabel(self)
        self.label_file.setText("File name")
        self.label_file.resize(140, 30)
        self.label_file.move(35, 30)

        self.text_file = QtWidgets.QLineEdit(self)
        self.text_file.resize(350, 22)
        self.text_file.move(30, 55)

        self.label_column = QtWidgets.QLabel(self)
        self.label_column.setText("Column name")
        self.label_column.resize(140, 30)
        self.label_column.move(35, 80)

        self.text_column = QtWidgets.QLineEdit(self)
        self.text_column.resize(350, 22)
        self.text_column.move(30, 105)

        self.label_data = QtWidgets.QLabel(self)
        self.label_data.setText("Amount of data")
        self.label_data.resize(140, 30)
        self.label_data.move(35, 130)

        self.text_amount = QtWidgets.QLineEdit(self)
        self.text_amount.setValidator(QtGui.QIntValidator(0, 10_000, self))
        self.text_amount.resize(350, 22)
        self.text_amount.move(30, 155)

        self.label_bins = QtWidgets.QLabel(self)
        self.label_bins.setText("Number of bins")
        self.label_bins.resize(140, 30)
        self.label_bins.move(35, 180)

        self.text_bins = QtWidgets.QLineEdit(self)
        self.text_bins.setValidator(QtGui.QIntValidator(0, 100, self))
        self.text_bins.resize(350, 22)
        self.text_bins.move(30, 205)

        self.label_imgname = QtWidgets.QLabel(self)
        self.label_imgname.setText("Name of the png file")
        self.label_imgname.resize(140, 30)
        self.label_imgname.move(35, 230)

        self.text_imgname = QtWidgets.QLineEdit(self)
        self.text_imgname.resize(350, 22)
        self.text_imgname.move(30, 255)

        self.img_label = QtWidgets.QLabel(self)
        self.img_label.setObjectName("img-label")
        self.img_label.resize(711, 525)
        self.img_label.move(420, 30)
        self.img_label.setText("Histogram")
        self.img_label.setAlignment(Qt.AlignCenter)

        self.button_histogram = QtWidgets.QPushButton(self)
        self.button_histogram.setText("Generate histogram")
        self.button_histogram.resize(350, 30)
        self.button_histogram.move(30, 290)
        self.button_histogram.clicked.connect(self.gen_hist)

        self.load_old_data()

    def load_old_data(self):
        """
        Load the data json file into the app input boxes.
        """
        self.text_file.setText(self.data.file.name)
        self.text_column.setText(self.data.column)
        self.text_amount.setText(str(self.data.amount))
        self.text_bins.setText(str(self.data.bins))
        self.text_imgname.setText(self.data.imgname)

    def get_app_data(self) -> Data:
        """
        Make a data object based of the content of the app input boxes.
        """
        return Data(
            file=Path.cwd() / self.text_file.text(),
            column=self.text_column.text(),
            amount=int(self.text_amount.text()),
            bins=int(self.text_bins.text()),
            imgname=self.text_imgname.text(),
        )

    def draw_image(self) -> None:
        """
        Pick up the image file and draw it on the app.
        """
        img_file = (
            self.data.imgname
            if self.data.imgname.endswith(".png")
            else self.data.imgname + ".png"
        )
        img_path = Path.cwd() / "img" / img_file

        img = QtGui.QPixmap(str(img_path))
        self.img_label.setPixmap(img)
        self.img_label.setScaledContents(True)

    def gen_hist(self):
        """
        Responsible for collecting the data from the app, provide the data to
        the histogram creation function, draw the image and then save the data
        provided by the app to the data file.
        """
        app_data: Data = self.get_app_data()

        self.create_hist_fn(app_data)

        self.draw_image()

        self.save_data_fn(app_data)
