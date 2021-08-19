import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
import sys


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
        self.setGeometry(self.spacing_left, self.spacing_top,
                         self.width, self.height)

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

        self.label_round = QtWidgets.QLabel(self)
        self.label_round.setText("Round coefficient")
        self.label_round.move(30, 230)

        self.text_round = QtWidgets.QLineEdit(self)
        self.text_round.resize(350, 22)
        self.text_round.move(30, 255)

        self.button_histogram = QtWidgets.QPushButton(self)
        self.button_histogram.setText("Make histogram")
        self.button_histogram.move(30, 290)
        self.button_histogram.clicked.connect(self.make_histogram)

    def make_histogram(self):
        file_name = self.text_file.text()
        column_name = self.text_column.text()
        number_of_data = int(self.text_data.text())
        number_of_bins = int(self.text_bins.text())
        round_coeff = int(self.text_round.text())

        table = pd.read_excel(file_name)
        data = table[column_name]
        data = [data[i] for i in range(number_of_data)]

        average = Equation.get_average(data)
        lower_bound = min(data)
        upper_bound = max(data)
        stand_dev = Equation.get_standard_deviation(
            data, average, number_of_data)

        channel_size = Equation.get_bin_size(
            lower_bound, upper_bound, number_of_bins)
        middle_values = Equation.get_middle_values(
            lower_bound, channel_size, number_of_bins)
        frequency = Equation.count_freq(
            data, middle_values, number_of_bins, channel_size, round_coeff)
        height_values = Equation.exp_prob_dens(
            frequency, number_of_data, channel_size)

        if sum(frequency) != number_of_data:
            print("Missing data")

        x = np.linspace(lower_bound, upper_bound, 1000)
        g_teo = Equation.theo_prob_dens(x, stand_dev, average)

        plt.bar(middle_values, height_values, channel_size)

        plt.plot(x, g_teo, 'r')
        plt.xlabel("x")
        plt.ylabel("Probability Density")

        plt.show()


class Equation:

    @staticmethod
    def get_average(arr):
        return sum(arr) / len(arr)

    @staticmethod
    def get_standard_deviation(arr, average, number):
        big_sum = 0
        for i in range(number):
            big_sum += (arr[i] - average)**2 / (number - 1)
        return np.sqrt(big_sum)

    @staticmethod
    def theo_prob_dens(x, stand_dev, average):
        return (1 / (stand_dev * np.sqrt(2 * np.pi))) * np.exp(-0.5 * (((x - average) / stand_dev)**2))

    @staticmethod
    def get_bin_size(min_val, max_val, chanels):
        return (max_val - min_val) / chanels

    @staticmethod
    def get_middle_values(min_val, channel_size, channel_count):
        values = []
        for i in range(channel_count):
            values.append(min_val + ((i + 1) - 0.5) * channel_size)
        return values

    @staticmethod
    def count_freq(arr, middle, channel_count, channel_size, round_coeff):
        values = [[]] * channel_count
        for i in range(channel_count):
            left_bound = np.round(middle[i] - channel_size / 2, round_coeff)
            right_bound = np.round(middle[i] + channel_size / 2, round_coeff)
            values[i] = [j for j in arr if j >= left_bound and j < right_bound]

        while values[0].count(min(arr)) < arr.count(min(arr)):
            values[0].append(min(arr))
        while values[channel_count - 1].count(max(arr)) < arr.count(max(arr)):
            values[channel_count - 1].append(max(arr))

        return [len(i) for i in values]

    @staticmethod
    def exp_prob_dens(arr, data_count, channel_size):
        frequency = list(map(lambda x: x / data_count, arr))
        prob_dens = list(map(lambda x: x / channel_size, frequency))
        return prob_dens


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = App()
    win.show()
    sys.exit(app.exec_())
