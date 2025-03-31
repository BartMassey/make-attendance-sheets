#!/usr/bin/python
import argparse
from datetime import datetime as dt
from dateutil import parser as dup
from dateutil.relativedelta import relativedelta as delta, MO, TU, WE, TH
from sys import stderr

# Known to work with fpdf2==2.8.2
# Also requires distro package fonts-dejavu-core by default.
from fpdf import fpdf

ap = argparse.ArgumentParser()
ap.add_argument("--start", help="start date (+<days>, <date>, default today)")
ap.add_argument("--students", help="student list file", default = "student-emails.txt")
ap.add_argument("--dest", help="output file", default = "attendance-sheets.pdf")
ap.add_argument("--font-path", default = "/usr/share/fonts/truetype")
ap.add_argument("course", help="course title")
ap.add_argument("days", help="meeting days (MUWH)")
ap.add_argument("count", type=int, help="number of meetings")
args = ap.parse_args()

def grab_name(s):
    p = s.find(" <")
    if p > 0:
        return s[:p]
    else:
        return s

try:
    with open(args.students, "r") as f:
        lines = f.read().splitlines()
        lines.sort(key=lambda s: s.split()[1])
        students = [grab_name(s) for s in lines]
except IOError as e:
    print(e, file=stderr)
    exit(1)

if len(args.days) == 0:
    print("must specify some days", file=stderr)
    exit(1)
day_names = "MUWH"
day_list = []
for d in args.days:
    di = day_names.find(d)
    if di == -1:
        print(f"unknown day {d}", file=stderr)
        exit(1)
    day_list.append(di)
    
s = args.start
if s is None:
    start = dt.now().date()
elif len(s) > 1 and s[0] == "+" and s[1:].isdigit():
    start = dt.now().date()
    start += delta(days=int(s[1:]))
else:
    start = dup.parse(args.start).date()

def first_day(start):
    return min(start + delta(weekday = d) for d in day_list)

start = first_day(start)
pdf = fpdf.FPDF(unit="pt", format="Letter")
pdf.add_font(
    "dejavu-sans",
    style="",
    fname=f"{args.font_path}/dejavu/DejaVuSans.ttf",
)
pdf.add_font(
    "dejavu-sans",
    style="B",
    fname=f"{args.font_path}/dejavu/DejaVuSans-Bold.ttf",
)
for _ in range(args.count):
    pdf.add_page()
    pdf.set_font('dejavu-sans', 'B', 16)
    date = start.strftime("%a %Y-%m-%d")
    header = "Attendance — " + " " + args.course + " — " + date + "\n\n"
    pdf.write(text=header)
    pdf.set_font('dejavu-sans', '', 16)
    with pdf.text_columns(
            text_align="L",
            ncols=2,
            gutter=5,
            line_height=1.5,
    ) as cols:
        for name in students:
            text = name + "\n"
            cols.write(text=text)

    start = first_day(start + delta(days=1))
try:
    pdf.output(name=args.dest)
except Exception as e:
    print(f"pdf output: {e}", file=stderr)
    exit(1)
