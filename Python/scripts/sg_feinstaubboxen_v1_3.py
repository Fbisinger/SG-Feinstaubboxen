# Feinstaubboxen Schelztor-Gymnasium v1.3
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
import pip
from backports.functools_lru_cache import lru_cache
import Tkinter as tk
from tkFileDialog import askopenfilename
import csv
from itertools import islice
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import tkMessageBox
from Tkinter import PhotoImage
import webbrowser
import ttk
#import time as t
#from Tkinter import *
#from PIL import ImageTk, Image
#import os

#TODO:
#add drag & drop capabillity => later[version 1.5]
#add menue bar => later[version 2.0 ???]
#add help/example menue
#add request before clear cache _/
#add section about _/
#add progress bar _/
#add number of datasets loaded _/
#add tooltips?? => maybe later
#add changing cursor _/
#fix bug (clear cache after opening new data) => Clear Cache button _/
#fix bug progressbar with big datasets
#add checkbox for progressbar (progressbar has negative influence to performance with big datasets)
#add error message after failed import _/
#add capability to compare several datasets => later[version1.4]

time = []
ID = []
temp = []
hum = []
pm10 = []
pm25 = []
pmall = []

i = 0
num_datasets = 0

def callback(url):
    webbrowser.open_new(url)

def get_help():
	#tkMessageBox.showinfo("Help", "HELP-TEXT --MISSING!!--")
	help_window = tk.Toplevel(root)
	help_window.title("Help      Feinstaubboxen Schelztor-Gymnasium (c) 2020 F.Bisinger v1.3")
	try:
		help_window.iconbitmap(sys._MEIPASS + '\\img\system_help.ico')
	except Exception:
				try:
					help_window.iconbitmap('C:\Users\Florian\Desktop\img\system_help.ico')
				except Exception:
					pass
	display = tk.Label(help_window, width=60, height=5, text="Further Help Information still missing. At the moment refer to:")
	display.pack()
	link1 = tk.Label(help_window, text="Website SG-Feinstaubboxen (https://github.com/Fbisinger/SG-Feinstaubboxen)", fg="blue", cursor="hand2")
	link1.pack()
	link1.bind("<Button-1>", lambda e: callback("https://github.com/Fbisinger/SG-Feinstaubboxen"))

def get_info():
	webbrowser.open('https://github.com/Fbisinger/SG-Feinstaubboxen', new=2)

def clear_cache_ask():
	if tkMessageBox.askyesno("Are you sure?","Will delete all cached Data!"):
		del time [:]
		del ID [:]
		del temp [:]
		del hum [:]
		del pm10 [:]
		del pm25 [:]
		del pmall [:]
		v.set("")
		progress_var.set(0)
		num_datasets = 0
		datasets_var.set("0 Datasets loaded")

def clear_cache():
		del time [:]
		del ID [:]
		del temp [:]
		del hum [:]
		del pm10 [:]
		del pm25 [:]
		del pmall [:]
		v.set("")
		progress_var.set(0)
		num_datasets = 0
		datasets_var.set("0 Datasets loaded")

def err_no_data():
	tkMessageBox.showerror("No Data selected", "You need to select your Data first!")

def err_unsupported_data():
	tkMessageBox.showerror("Unsupported Data", "This Data/Datatype/Formatting is not supported!\nPlease refer to Help...")

def show_logo():
	try:
		plt.get_current_fig_manager().window.wm_iconbitmap(sys._MEIPASS + '\\img\logo.ico')
	except Exception:
				try:
					plt.get_current_fig_manager().window.wm_iconbitmap('C:\Users\Florian\Desktop\img\logo.ico')
				except Exception:
					pass

def plot_temp():
	if len(ID) > 0:
		plt.get_current_fig_manager().canvas.set_window_title('SG-Feinstaubboxen-Temperature')
		show_logo()
		plt.plot(ID, temp, 'o-', label='Temperature(C)')
		plt.ylabel('Temperature')
		print('\n')
		print(time[0])
		print('-')
		print(time[len(time)-1])
		plt.xlabel('ID (' + time[0] + ' - ' + time[len(time)-1] + ')')
		plt.title('Feinstaubboxen Schelztor-Gymnasium (c) 2020 F.Bisinger ')
		plt.legend()
		plt.show()
	else:
		err_no_data()

def plot_hum():
	if len(ID) > 0:
		plt.get_current_fig_manager().canvas.set_window_title('SG-Feinstaubboxen-Humidity')
		show_logo()
		plt.plot(ID, hum, 'o-', label='relative Humidity(%)')
		plt.ylabel('Humidity')
		print('\n')
		print(time[0])
		print('-')
		print(time[len(time)-1])
		plt.xlabel('ID (' + time[0] + ' - ' + time[len(time)-1] + ')')
		plt.title('Feinstaubboxen Schelztor-Gymnasium (c) 2020 F.Bisinger ')
		plt.legend()
		plt.show()
	else:
		err_no_data()

def plot_pm10():
	if len(ID) > 0:
		plt.get_current_fig_manager().canvas.set_window_title('SG-Feinstaubboxen-PM10')
		show_logo()
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
	else:
		err_no_data()

def plot_pm25():
	if len(ID) > 0:
		plt.get_current_fig_manager().canvas.set_window_title('SG-Feinstaubboxen-PM25')
		show_logo()
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
	else:
		err_no_data()

def plot_pmall():
	if len(ID) > 0:
		plt.get_current_fig_manager().canvas.set_window_title('SG-Feinstaubboxen-PM-All')
		show_logo()
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
	else:
		err_no_data()
	
def import_csv_data():
	#clear_cache()
	i = 0
	global v
	csv_file_path = askopenfilename()
	print("File Path: " + csv_file_path)
	v.set(csv_file_path)

	num_datasets = sum(1 for line in open(csv_file_path)) - 24
	print("Number of Datasets: " + str(num_datasets))
	pb["maximum"] = num_datasets

	with open(csv_file_path, "r") as csvfile:
		try:
			for row in islice(csv.reader(csvfile), 24, None):
				progress_var.set(i + 1)
				datasets_var.set(str(i + 1) + " Datasets loaded")
				#print(row)
				ID.append(float(i))
				i = i+1
			
				time.append(str(row[0]))
				temp.append(float(row[1]))
				hum.append(float(row[2]))
				pm10.append(float(row[3]))
				pm25.append(float(row[4]))

				root.update_idletasks()
		except:
			err_unsupported_data()
			clear_cache()


root = tk.Tk()
root.title("Feinstaubboxen Schelztor-Gymnasium (c) 2020 F.Bisinger v1.3")
try:
	root.iconbitmap(sys._MEIPASS + '\\img\logo.ico')
except Exception:
            try:
				root.iconbitmap('C:\Users\Florian\Desktop\img\logo.ico')
            except Exception:
                pass
#root.iconbitmap(sys._MEIPASS + '\\logo.ico')
tk.Label(root, text='File Path').grid(row=0, column=0)
tk.Label(root, text='This Script, written and debugged \n in Python by Florian Bisinger \n is a tool to create simple plots \n from csv-files').grid(row=0, column=2)
#img = ImageTk.PhotoImage(Image.open("Logo_SG_Digitalisierung.jpg"))
#panel = Label(root, image = img)
#panel.pack(side = "bottom", fill = "both", expand = "yes")
v = tk.StringVar()
entry = tk.Entry(root, textvariable=v).grid(row=0, column=1)
tk.Button(root, text='Browse Data Set',command=import_csv_data, cursor="hand2").grid(row=1, column=0)
tk.Button(root, text='Generate Plot Temperature',command=plot_temp, cursor="hand2").grid(row=2, column=0)
tk.Button(root, text='Generate Plot Humidity',command=plot_hum, cursor="hand2").grid(row=2, column=1)
tk.Button(root, text='Generate Plot PM10',command=plot_pm10, cursor="hand2").grid(row=2, column=2)
tk.Button(root, text='Generate Plot PM2.5',command=plot_pm25, cursor="hand2").grid(row=2, column=3)
tk.Button(root, text='Generate Plot PMall',command=plot_pmall, cursor="hand2").grid(row=2, column=4)
tk.Button(root, text='Clear Cache',command=clear_cache_ask, cursor="hand2").grid(row=1, column=1)
tk.Button(root, text='About...',command=get_info, cursor="question_arrow").grid(row=1, column=2)
tk.Button(root, text='Help...',command=get_help, cursor="question_arrow").grid(row=1, column=3)
tk.Button(root, text='Close',command=root.destroy, cursor="hand2").grid(row=1, column=4)

progress_var = tk.IntVar()
pb = ttk.Progressbar(root, orient="horizontal", length=100, mode="determinate", var=progress_var)
pb.grid(row=0,column=3)
pb["value"] = 0

datasets_var = tk.StringVar()
datasets_var.set("0 Datasets loaded")
tk.Label(root, textvariable=datasets_var).grid(row=0, column=4)

root.mainloop()
