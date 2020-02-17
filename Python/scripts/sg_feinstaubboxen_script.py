# Feinstaubboxen Schelztor-Gymnasium Arduino Script
#      (c) 2020 F.Bisinger
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import csv
from itertools import islice
import matplotlib.pyplot as plt
#import numpy as np

time = []
ID = []
temp = []
hum = []
pm10 = []
pm25 = []
pmall = []
#temphum = []
i = 0

u_input = input("Filename (STANDART FILE LOCATION: DESKTOP! use quotation marks, no need of file extension): ")
filename = u_input + ".TXT"
with open(filename, "r") as csvfile:
    	for row in islice(csv.reader(csvfile), 24, None):
        	print(row)
        	ID.append(float(i))
       		i = i+1
       		
       		time.append(str(row[0]))
    		temp.append(float(row[1]))
    		hum.append(float(row[2]))
       		pm10.append(float(row[3]))
       		pm25.append(float(row[4]))
       		
	input_var = input("Enter temp/hum/pm10/pm25/pmall: ")
	print ("you entered " + str(input_var))    	
	
for x in range(len(ID)): 
	print ID[x],
if input_var == temp:    
	plt.plot(ID, temp, 'o-', label='Temperatur(C)')
	plt.ylabel('Temperatur')
	
if input_var == hum:
	plt.plot(ID, hum, 'o-', label='Relative Luftfeuchtigkeit(%)')
	plt.ylabel('Luftfeuchtigkeit')
	
if input_var == pm10:
	plt.plot(ID, pm10, 'o-', label='pm10(ug/m^3)')
	plt.ylabel('pm 10')
	
if input_var == pm25:
	plt.plot(ID, pm25, 'o-', label='pm2.5(ug/m^3)')
	plt.ylabel('pm 2.5')
	
if input_var == pmall:
	plt.plot(ID, pm10, 'o-', label='pm10(ug/m^3)')
	plt.plot(ID, pm25, 'o-', label='pm2.5(ug/m^3)')
	plt.ylabel('pm10/pm2.5')
	
#if input_var == temphum:
#	plt.plot(ID, temp, 'o-', label='Temperatur(C)')
#	plt.plot(ID, hum, 'o-', label='Relative Luftfeuchtigkeit(%)')
#	plt.ylabel('Temperatur/Luftfeuchtigkeit')
	
print('\n')
print(time[0])
print('-')
print(time[len(time)-1])
plt.xlabel('ID (' + time[0] + ' - ' + time[len(time)-1] + ')')
plt.title('Feinstaubboxen Schelztor-Gymnasium (c) 2020 F.Bisinger ')
plt.legend()
plt.show()        
