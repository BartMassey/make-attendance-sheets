# make-attendance-sheets: Make attendance sheets
Bart Massey 2024

This little piece of Python is what I use to make my
attendance sheets. 

The program takes a class title, a spec for what days my
class meets, and a count of sheets to print.  It also
implicitly looks for a list of my students (with optional
email address which will be stripped) and a start date to
print sheets from.

The output is a single PDF containing the attendance sheets.

The program does the math to skip forward to the first
weekday listed in its spec and then skip forward by
successive weekdays. Currently the only weekdays supported
are "MUWH" for Monday, Tuesday, Wednesday, Thursday: that's
all I ever teach on.

# License

This work is licensed under the "MIT License". Please see the file
`LICENSE.txt` in this distribution for license terms.
