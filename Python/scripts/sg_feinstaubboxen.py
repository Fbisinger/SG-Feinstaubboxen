# Feinstaubboxen Schelztor-Gymnasium
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

import Tkinter as tk
from tkFileDialog import askopenfilename
import csv
from itertools import islice
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
#from Tkinter import *
#from PIL import ImageTk, Image
#import os

time = []
ID = []
temp = []
hum = []
pm10 = []
pm25 = []
pmall = []

global i

def plot_temp():
	plt.plot(ID, temp, 'o-', label='Temperatur(C)')
	plt.ylabel('Temperatur')
	print('\n')
	print(time[0])
	print('-')
	print(time[len(time)-1])
	plt.xlabel('ID (' + time[0] + ' - ' + time[len(time)-1] + ')')
	plt.title('Feinstaubboxen Schelztor-Gymnasium (c) 2020 F.Bisinger ')
	plt.legend()
	plt.show()

def plot_hum():
	plt.plot(ID, hum, 'o-', label='Relative Luftfeuchtigkeit(%)')
	plt.ylabel('Luftfeuchtigkeit')
	print('\n')
	print(time[0])
	print('-')
	print(time[len(time)-1])
	plt.xlabel('ID (' + time[0] + ' - ' + time[len(time)-1] + ')')
	plt.title('Feinstaubboxen Schelztor-Gymnasium (c) 2020 F.Bisinger ')
	plt.legend()
	plt.show() 

def plot_pm10():
	plt.plot(ID, pm10, 'o-', label='pm10(ug/m^3)')
	plt.ylabel('pm10')	
	print('\n')
	print(time[0])
	print('-')
	print(time[len(time)-1])
	plt.xlabel('ID (' + time[0] + ' - ' + time[len(time)-1] + ')')
	plt.title('Feinstaubboxen Schelztor-Gymnasium (c) 2020 F.Bisinger ')
	plt.legend()
	plt.show() 

def plot_pm25():
	plt.plot(ID, pm25, 'o-', label='pm2.5(ug/m^3)')
	plt.ylabel('pm2.5')	
	print('\n')
	print(time[0])
	print('-')
	print(time[len(time)-1])
	plt.xlabel('ID (' + time[0] + ' - ' + time[len(time)-1] + ')')
	plt.title('Feinstaubboxen Schelztor-Gymnasium (c) 2020 F.Bisinger ')
	plt.legend()
	plt.show()

def plot_pmall():
	plt.plot(ID, pm10, 'o-', label='pm10(ug/m^3)')
	plt.plot(ID, pm25, 'o-', label='pm2.5(ug/m^3)')
	plt.ylabel('pm10/pm2.5')	
	print('\n')
	print(time[0])
	print('-')
	print(time[len(time)-1])
	plt.xlabel('ID (' + time[0] + ' - ' + time[len(time)-1] + ')')
	plt.title('Feinstaubboxen Schelztor-Gymnasium (c) 2020 F.Bisinger ')
	plt.legend()
	plt.show() 
	
def import_csv_data():
	i = 0
	global v
	csv_file_path = askopenfilename()
	print(csv_file_path)
	v.set(csv_file_path)

	with open(csv_file_path, "r") as csvfile:
		for row in islice(csv.reader(csvfile), 24, None):
			print(row)
			ID.append(float(i))
			i = i+1
		
			time.append(str(row[0]))
			temp.append(float(row[1]))
			hum.append(float(row[2]))
			pm10.append(float(row[3]))
			pm25.append(float(row[4]))

root = tk.Tk()
root.title("Feinstaubboxen Schelztor-Gymnasium (c) 2020 F.Bisinger")
tk.Label(root, text='File Path').grid(row=0, column=0)
tk.Label(root, text='This Script, written and debugged \n in Python by Florian Bisinger \n is a tool to create simple plots \n from csv-files').grid(row=0, column=2)
#img = ImageTk.PhotoImage(Image.open("Logo_SG_Digitalisierung.jpg"))
#panel = Label(root, image = img)
#panel.pack(side = "bottom", fill = "both", expand = "yes")
v = tk.StringVar()
entry = tk.Entry(root, textvariable=v).grid(row=0, column=1)
tk.Button(root, text='Browse Data Set',command=import_csv_data).grid(row=1, column=0)
tk.Button(root, text='Generate Plot Temperature',command=plot_temp).grid(row=2, column=0)
tk.Button(root, text='Generate Plot Humidity',command=plot_hum).grid(row=2, column=1)
tk.Button(root, text='Generate Plot PM10',command=plot_pm10).grid(row=2, column=2)
tk.Button(root, text='Generate Plot PM2.5',command=plot_pm25).grid(row=2, column=3)
tk.Button(root, text='Generate Plot PMall',command=plot_pmall).grid(row=2, column=4)
tk.Button(root, text='Close',command=root.destroy).grid(row=1, column=1)
root.mainloop()
