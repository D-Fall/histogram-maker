import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
import sys
import json

DATA = "./data.json"


class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        self.width = 500
        self.height = 400
        self.title = "Histogram Maker"
        self.spacing_left = 200
        self.spacing_top = 200
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.spacing_left, self.spacing_top, self.width, self.height)

        self.label_file = QtWidgets.QLabel(self)
        self.label_file.setText("File name")
        self.label_file.move(30, 30)

        self.text_file = QtWidgets.QLineEdit(self)
        self.text_file.resize(350, 22)
        self.text_file.move(30, 55)

        self.label_column = QtWidgets.QLabel(self)
        self.label_column.setText("Column name")
        self.label_column.move(30, 80)

        self.text_column = QtWidgets.QLineEdit(self)
        self.text_column.resize(350, 22)
        self.text_column.move(30, 105)

        self.label_data = QtWidgets.QLabel(self)
        self.label_data.setText("Amount of data")
        self.label_data.move(30, 130)

        self.text_data = QtWidgets.QLineEdit(self)
        self.text_data.resize(350, 22)
        self.text_data.move(30, 155)

        self.label_bins = QtWidgets.QLabel(self)
        self.label_bins.setText("Number of bins")
        self.label_bins.move(30, 180)

        self.text_bins = QtWidgets.QLineEdit(self)
        self.text_bins.resize(350, 22)
        self.text_bins.move(30, 205)

        self.button_histogram = QtWidgets.QPushButton(self)
        self.button_histogram.setText("Make histogram")
        self.button_histogram.move(30, 290)
        self.button_histogram.clicked.connect(self.make_histogram)

    def make_histogram(self):
        file_name = self.text_file.text()
        column_name = self.text_column.text()
        number_of_data = int(self.text_data.text())
        number_of_bins = int(self.text_bins.text())

        table = pd.read_excel(file_name)
        data: list[float] = table[column_name][:number_of_data]

        average = np.mean(data)
        lower_bound = min(data)
        upper_bound = max(data)
        stand_dev = np.std(data)

        x = np.linspace(lower_bound, upper_bound, 1000)
        g_teo = get_normal_distribution(x, stand_dev, average)

        plt.hist(data, bins=number_of_bins, density=True)

        plt.plot(x, g_teo, "r", label="Normal distribution")
        plt.xlabel("$x$")
        plt.ylabel("Density")
        plt.legend()

        plt.show()


def get_normal_distribution(x_range, std, mean):
    return (1 / (std * np.sqrt(2 * np.pi))) * np.exp(
        -0.5 * (((x_range - mean) / std) ** 2)
    )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = App()
    win.show()
    sys.exit(app.exec_())
