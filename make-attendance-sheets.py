#!/usr/bin/python
import argparse
from datetime import datetime as dt
from dateutil import parser as dup
from dateutil.relativedelta import relativedelta as delta, MO, TU, WE, TH
from fpdf import FPDF
from sys import stderr

ap = argparse.ArgumentParser()
ap.add_argument("--start", help="start date (+<days>, <date>, default today)")
ap.add_argument("--students", help="student list file", default = "student-emails.txt")
ap.add_argument("--dest", help="output file", default = "attendance.pdf")
ap.add_argument("course", help="course title")
ap.add_argument("days", help="meeting days (MUWH)")
ap.add_argument("count", type=int, help="number of meetings")
args = ap.parse_args()

try:
    with open(args.students, "r") as f:
        students = f.read()
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

for _ in range(args.count):
    print(start)
    start = first_day(start + delta(days=1))
