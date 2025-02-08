#! /usr/bin/python
# -*- coding: utf-8 -*-
# etcal.py v1.1
# Python script to display Ethiopian Calendar
# Usage etcal.py [Year] [Month]
# Author th3snk@yahoo.com
#
from __future__ import print_function
import sys
import datetime

class EtDate:
  def __init__(self, year, month, day):
    self.year = year
    self.month = month
    self.day = day
  def display(self):
    print(self.year, self.month, self.day)

def usage(message):
  print(message)
  print("Usage ", sys.argv[0]," [Year] [Month]")
  print("For example ", sys.argv[0])
  print("            ", sys.argv[0]," 1888")
  print("            ", sys.argv[0]," 1888 6")
  exit(1)

def getMonthName(month):
  months = ['መ ስከረም ', 'ጥ ቅ ም ት', 'ሕ ዳ ር', 'ታ ሕ ሣ ስ', 'ጥ ር', 'የካቲት', 'መ ጋቢት', 'ሚ ያዚያ', 'ግንቦት', 'ሰኔ', 'ሐ ም ሌ', 'ነሐ ሴ', 'ጳጉሜ ']
  return months[month-1]

def etToday():
  now = datetime.datetime.now()
  gyear = now.year
  gmonth = now.month
  gday = now.day

  isLastYearLeap = (gyear - 7) % 4	#lastYear=gyear-8 but to check leap (year+1)%4
  if gmonth < 9:
    tyear = gyear - 8
  elif gmonth > 9:
    tyear = gyear - 7
  else:
    if (gday < 11 or (gday == 11 and isLastYearLeap == 0)):
      tyear = gyear - 8
    else:
      tyear = gyear - 7

  #check if the year before is leap (tyear-1+1)%4
  start = 11	#this year started on september 11
  if tyear % 4 == 0:
    start = 12
  total = 31 - start	 #days left in september

  nstart = start	#next year starts on september 11 or 12
  if (isLastYearLeap == 0 and (tyear + 1) % 4 == 0):
    nstart = 12

  if (gmonth == 9 and gday >= nstart):
    tmonth = 1
    tday = gday - start + 1
  else:
    for i in [10, 11, 12, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
      if i == gmonth:
        total = total + gday
        tmonth = (total / 30) + 1
        tday = total % 30
        if tday == 0:
          tmonth = tmonth - 1
          tday = 30
        break
      else:
        if (i == 4 or i == 6 or i == 9 or i == 11):
          total = total + 30
        elif i == 2:
          if (gyear % 4 != 0 or (gyear % 100 == 0 and gyear % 400 != 0)):
            total = total + 28
          else:
            total = total + 29
        else:
          total = total + 31

  etoday = EtDate(tyear, tmonth, tday)

  return etoday

if len(sys.argv) > 3:
  usage(' ')
elif len(sys.argv) > 1:
  year = int(sys.argv[1])
  if year < 0:
    usage('Year should be a positive number')
  elif len(sys.argv) > 2:
    month = int(sys.argv[2])
    day = 0
    if (month < 1 or month > 13):
      usage('Month should be from 1 to 13')
  else:
    month = 1
    day = 0
else:
  etnow = etToday()
  year = etnow.year
  month = etnow.month
  day = etnow.day

newYear = (year * 5 / 4 + 2) % 7	#starting date of the year assuming sun=0, mon=1 ... sat=6

#start printing to stdout
noOfMonths = 1
if len(sys.argv) == 2:	#if only year is given as argument
  print("      ", year)
  noOfMonths = 13
for j in range(0, noOfMonths):
  monthStart = (newYear + month * 2 - 2) % 7
  monthName = getMonthName(month)
  if noOfMonths == 13:
    print("      ", monthName)
  else:
    print("    ", monthName, year)
  print(" እ  ሰ  ማ  ረ  ኀ  አ  ቅ")
  for i in range(0, monthStart):
    print("   ", end='')
  noOfDays = 30
  if(month == 13 and (year + 1) % 4 == 0):
    noOfDays = 6
  elif(month == 13 and (year + 1) % 4 != 0):
    noOfDays = 5
  for i in range(1, noOfDays + 1):
    if(i == etToday().day and year == etToday().year and month == etToday().month):
      print("\033[42m", end='')	#change bg color of today
    if i > 9:
      print(i,end='')
    else:
      print("", i, end='')
    if(i == etToday().day and year == etToday().year and month == etToday().month):
      print("\033[00m", end='')	#change back bg color of today
    print(" ",end='')	#separetor b/n days
    if(i + monthStart) % 7 == 0:	#end of week
      print(' ')	#print new line
  month = month + 1
  print(' ')
