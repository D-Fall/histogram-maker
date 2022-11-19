# The Histogram Maker

This is a personal project that started as a way to automate a boring task for
university. Then I realized that so many frameworks already did what I ment to
do. As a result, I've been using it for the past year to test new skills
reguarding coding in general, like making a GUI, design patters, software
architecture and unit testing, to name a few.

## What is does

It is an app, executed via console, that reads a spreadsheet file (Excel,
xlsx) and plots for you a histogram with the normal distribution included.

## Packages used

- matplotlib
- SciencePlots
- numpy
- scipy
- pandas
- xlrd
- openpyxl
- PyQt5

## Instructions

1. Make sure that your table is in the same folder as your program. The
   repository already comes with a sample table called **test.xlsx**.

2. Run the Python app the way you prefer, by command line or button inside an
   IDE, then the app will ask you some questions:

- **File name** is just the name of the file with extention;
- **Column name** is the column that the program will read;
- **Amount of data** is the number of data that the app will analyze to make the
  histogram;
- **Number of bins** is how many columns (bins) you want in your histogram. A
  good reference value is an odd number close to the square root of the amount of
  data;
- **Name of the png file** is the name of the file that will be saved at a file
  called _/img_ in the directory of the project. Change the name and you can have
  multiple images. Leave the same name and the image will be updated. You don't
  need to put the _.png_ at the end.

3. Now click the button to generate the histogram. You can check the saved file
   after.

# TODO

1. Make a way to take a path to a spreadsheet file.
2. Make a way to recieve integers from the input boxes

   - Study about QDoubleValidator

3. Save integers
