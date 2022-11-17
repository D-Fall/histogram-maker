import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import norm

from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import Qt

import sys
import json
from pathlib import Path

plt.style.use(["science", "notebook", "grid"])
DATA = "./data.json"
STYLESHEET = "./styles.css"


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.width = 800
        self.height = 700
        self.title = "Histogram Maker"
        self.spacing_left = 200
        self.spacing_top = 200
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.spacing_left, self.spacing_top, self.width, self.height)

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

        self.text_data = QtWidgets.QLineEdit(self)
        self.text_data.resize(350, 22)
        self.text_data.move(30, 155)

        self.label_bins = QtWidgets.QLabel(self)
        self.label_bins.setText("Number of bins")
        self.label_bins.resize(140, 30)
        self.label_bins.move(35, 180)

        self.text_bins = QtWidgets.QLineEdit(self)
        self.text_bins.resize(350, 22)
        self.text_bins.move(30, 205)

        self.label_imgname = QtWidgets.QLabel(self)
        self.label_imgname.setText("Name of the png file")
        self.label_imgname.resize(140, 30)
        self.label_imgname.move(35, 230)

        self.text_imgname = QtWidgets.QLineEdit(self)
        self.text_imgname.resize(350, 22)
        self.text_imgname.move(30, 255)

        self.button_histogram = QtWidgets.QPushButton(self)
        self.button_histogram.setText("Make histogram")
        self.button_histogram.resize(350, 30)
        self.button_histogram.move(30, 290)
        self.button_histogram.clicked.connect(self.make_histogram)

        self.img_label = QtWidgets.QLabel(self)
        self.img_label.setObjectName("img-label")
        self.img_label.resize(711, 525)
        self.img_label.move(420, 30)
        self.img_label.setText("Histogram")
        self.img_label.setAlignment(Qt.AlignCenter)

        self.load_data()

    def load_data(self):
        self.data: dict = load_json(DATA)
        self.text_file.setText(self.data["file"])
        self.text_column.setText(self.data["column"])
        self.text_data.setText(self.data["data"])
        self.text_bins.setText(self.data["bins"])
        self.text_imgname.setText(self.data["imgname"])

    def make_histogram(self):
        file_name = self.text_file.text()
        self.data["file"] = file_name

        column_name = self.text_column.text()
        self.data["column"] = column_name

        number_of_data = self.text_data.text()
        self.data["data"] = number_of_data
        if number_of_data.isdigit():
            number_of_data = int(number_of_data)
        else:
            raise ValueError("Number of data needs to be an integer.")

        number_of_bins = self.text_bins.text()
        self.data["bins"] = number_of_bins
        if number_of_bins.isdigit():
            number_of_bins = int(number_of_bins)
        else:
            raise ValueError("Number of bins needs to be an integer.")

        img_name = self.text_imgname.text()
        self.data["imgname"] = img_name

        update_file(DATA, self.data)

        table = pd.read_excel(file_name)
        data: list[float] = table[column_name][:number_of_data]

        average = np.mean(data)
        lower_bound = min(data)
        upper_bound = max(data)
        stand_dev = np.std(data)

        x = np.linspace(lower_bound, upper_bound, 100)
        f = norm.pdf(x, average, stand_dev)

        plt.hist(data, bins=number_of_bins, density=True)
        plt.plot(x, f, "r", label="Normal distribution")
        plt.xlabel("$x$")
        plt.ylabel("Density")
        plt.legend()
        plt.savefig(f"./img/{img_name}.png", dpi=200)

        histogram_img = QtGui.QPixmap(f"./img/{img_name}.png")
        self.img_label.setPixmap(histogram_img)
        self.img_label.setScaledContents(True)


def load_json(filepath: str) -> dict:
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "file": "",
            "column": "",
            "data": "",
            "bins": "",
            "imgname": "histogram",
        }
    except json.JSONDecodeError:
        return {
            "file": "",
            "column": "",
            "data": "",
            "bins": "",
            "imgname": "histogram",
        }


def update_file(filepath: str, data: dict) -> None:
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = App()
    stylesheet = Path(STYLESHEET).read_text()
    win.setStyleSheet(stylesheet)
    win.show()
    sys.exit(app.exec_())
