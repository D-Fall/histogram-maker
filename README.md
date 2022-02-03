# Welcome to the first version of the Histogram Maker

This is an app, executed via console, that reads an Excel file and plots for you a histogram with the normal distribution included.

## Packages used

- matplotlib
- numpy
- pandas
- xlrd
- openpyxl
- PyQt5

## Instructions

First thing, you want to make sure that your table is in the same folder as your program. The repository already comes with a sample table called **test.xlsx**.

Run the program by typping one of those 3 commands. The one for you will depend on your Python settings and your OS.

- py app.py
- python app.py
- python3 app.py

Then the app will ask you some questions.

- **File name** is just the name of the file with extention;
- **Column name** is the column that the program will read;
- **Amount of data** is the number of data that the app will analyze to make the histogram;
- **Number of bins** is how many columns you want in your histogram;
- **Name of the png file** is the name of the file that will be saved at a file called _/img_ in the directory of the project. Change the name and you can have multiple images. Leave the same name and the image will be updated. You don't need to put the _.png_ at the end.

## TO DO

- Add a stylesheet
