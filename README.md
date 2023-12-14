## Installing Python
This goes without saying, but you need Python installed to run these files. If you have a Linux VM you are probably good to go.
If you are on a Windows machine or are inexperienced with Python, you can run python files at https://www.online-python.com/.
Simply download all the files in this repository, upload them to the website, and make the necessary modifications as outlined below.


## How it works
Three Python files process text (.txt) and comma-separated values (.csv) files separately for creating watchbills. This guide will tell you how to make the .txt files and .csv files. All of your files must be in the same directory for the python files to work.


## Deliberation
This is important as you will be defining the days on which watch will be assigned, as well as the point-value for each day.
After polling my company via Google Form, I found that the majority agreed on this point distribution:

Normal Week:

`Weekdays: 1.00`

`Friday:   1.75`

`Saturday: 2.00`

`Sunday:   1.75`

Three-Day:

`Friday:   2.25`

`Saturday: 2.50`

`Sunday:   2.50`

`Monday:   2.25`

Special:

`Day before leave: 2.5`

`Day returning from leave: 1.5`

After deciding, update your Multiplier column in your Google Sheets company watchbill. MAKE SURE YOU DELETE VALUES ON DAYS WATCH IS STOOD DOWN

![image](https://github.com/mangogenerator/adj/assets/150052846/9fdd6ff4-8eb5-495e-a39f-fabf4591bde5)


## Initial Setup
1. Copy the values in the two rows from the Google Sheet containing the numerical date and the day of the week and paste them into an Excel spreadsheet. Include the header row. The format of the date does not matter, use whatever format works best for you.

![image](https://github.com/mangogenerator/adj/assets/150052846/d6e68833-6faf-49f4-a83e-2b734bf6bd7a)

2. Next, copy the multiplier column into that same Excel spreadsheet. 

![image](https://github.com/mangogenerator/adj/assets/150052846/cdbe54a3-9169-47e9-8642-006d4de9439b)

3. Delete rows on which watch will not be stood (i.e. Thanksgiving Break, Spring Break). Confirm with brigade adj which days will be stood down.

4. Save the file as `days_static.csv`. This file will be used by all three Python programs.

## CDO Assignment
1. You will need a list of all the firsties who will be standing CDO this semester.
2. Open a text editor such as __Notepad__ and type in names line-by-line. Should look like this:
   
![image](https://github.com/mangogenerator/adj/assets/150052846/41ab3f1b-926c-4e6a-8826-2c431c5a3b86)

3. Save the file as `cdo.txt`.
4. Run `cdo.py`.
5. Three files are generated. Check `CDO_ASSIGNMENTS.txt` and `CDO_ASSIGNMENTS_BY_LASTNAME.csv` to see how many points each person got, and which dates they have, respectively. If you like what you see, open up `CDO_WATCHBILL.csv` in Excel and you can copy and paste the column with the lastnames into your Google Sheets watchbill.
6. If you think the watchbill isn't fair, there is one parameter in cdo.py that you can change:

![image](https://github.com/mangogenerator/adj/assets/150052846/d5ba872d-9454-490b-be93-4a211c6b7f53)

This is the minimum number of days between watches. The number is set at 8 but if the watchbill is generating unfairly, try decreasing the number.


## ACDO Assignment
1. The steps are basically the same. Get the list of people standing ACDO.
2. Make the `acdo.txt` file the same way you made the cdo.txt file.
3. Run `acdo.py`.
4. Same results as `cdo.py` except for `acdo.py` you obviously get two people each day.
5. You can try changing the `days_between_should_be` variable on line 3 of `acdo.py` to try to make it more even. It is currently set to 5.

## Duty Section Assignment
1. Find out how many duty sections you will have. I made 9 duty sections as each duty section requires 10 people. Check the numbers, YMMV.
2. Make a text file with 1 number per line, like this:

![image](https://github.com/mangogenerator/adj/assets/150052846/47764a00-5588-4917-a3de-e11f5efc357d)

3. Save it as `duty_sections.txt`.
4. Run `ds.py`.
5. Same results as `cdo.py` except you will get duty section numbers.
6. You can try changing the `days_between_should_be` variable on line 3 of `ds.py` to try to make it more even. It is currently set at 8.


## Extra Files
Example files (the ones I used) are in the example folder if you want to check format.





















