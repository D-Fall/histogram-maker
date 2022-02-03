# Welcome to the first version of the Histogram Maker

This is an app, executed via console, that reads an Excel file and plots for you a histogram with the gaussian distribution included.

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
- **Round coeffitient** is how many decimal places the app will round at the lower and upper bounds of each bin interval.

## Disclaimer

If the number of data in the final histogram isn't the same as the number of data analyzed, then the program will tell you that data is missing in the console. If this happens, maybe your round coeffitient is too low, but if it is not the case, then the code has a bug that should be fixed. Please, report if it happens to you.

## TO DO

- Add a stylesheet
