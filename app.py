import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd 

def main():
    file_name = input("File name: ")
    column_name = input("Column name: ")
    number_of_data = int(input("Amount of data: "))
    number_of_channels = int(input("Number of bins: "))
    round_coeff = int(input("Round coeffitient: "))

    table = pd.read_excel(file_name)
    data = table[column_name]
    data = [data[i] for i in range(number_of_data)]
    
    average = calculate_average(data)
    lower_bound = min(data)
    upper_bound = max(data)
    stand_dev = calculate_stand_dev(data, average, number_of_data)

    channel_size = calculate_channel_size(lower_bound, upper_bound, number_of_channels)
    middle_values = calculate_middle_values(lower_bound, channel_size, number_of_channels)
    frequency = count_freq(data, middle_values, number_of_channels, channel_size, round_coeff)
    height_values = exp_prob_dens(frequency, number_of_data, channel_size)
    
    plt.bar(middle_values, height_values, channel_size)


    if sum(frequency) != number_of_data:
        print("Missing data")


    x = np.linspace(lower_bound, upper_bound, 1000)
    g_teo = (1 / (stand_dev * np.sqrt(2 * np.pi))) * np.exp(-0.5 * (((x - average) / stand_dev)**2))
    
    plt.plot(x, g_teo, 'r')
    plt.xlabel("x")
    plt.ylabel("Probability Density")

    plt.show()


def calculate_average(arr):
    return sum(arr) / len(arr)


def calculate_stand_dev(arr, average, number):
    big_sum = 0
    for i in range(number):
        big_sum += (arr[i] - average)**2 / (number - 1)
    return np.sqrt(big_sum)


def theo_prob_dens(x, stand_dev, average):
    return (1 / (stand_dev * np.sqrt(2 * np.pi))) * np.exp(-0.5 * (((x - average) / stand_dev)**2))


def calculate_channel_size(min_val, max_val, chanels):
    return (max_val - min_val) / chanels


def calculate_middle_values(min_val, channel_size, channel_count):
    values = []
    for i in range(channel_count):
        values.append(min_val + ((i + 1) - 0.5) * channel_size)
    return values


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


def exp_prob_dens(arr, data_count, channel_size):
    frequency = list(map(lambda x: x / data_count, arr))
    prob_dens = list(map(lambda x: x / channel_size, frequency))
    return prob_dens


if __name__ == "__main__":
    main()