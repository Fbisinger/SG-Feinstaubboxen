# Feinstaubboxen Schelztor-Gymnasium v1.5
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
from TkinterDnD2 import *
#import time as t
#from Tkinter import *
#from PIL import ImageTk, Image
#import os

#TODO:
#add drag & drop capabillity => later[version 1.4] _/ (1.4)
#add exception handeling after multiple data import _/ (1.4)
#add menue bar => later[version 2.0 ???]
#add help/example menue _/ (1.5)
#add request before clear cache _/
#add section about _/
#add progress bar _/
#add number of datasets loaded _/
#add tooltips?? => maybe later
#add changing cursor _/
#fix bug (clear cache after opening new data) => Clear Cache button _/
#fix bug progressbar with big datasets
#(add checkbox for progressbar (progressbar has negative influence to performance with big datasets))
#add error message after failed import _/
#add capability to compare several datasets => later[version2.0 ???]
#add exception handeling at askopenfile dialog _/ (1.4)
#fix minor mistake at "clear cache" _/ (1.5)
#MAKE A GERMAN VERSION / I18N!

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
	help_window.title("Help      Feinstaubboxen Schelztor-Gymnasium (c) 2020 F.Bisinger v1.5")
	try:
		help_window.iconbitmap(sys._MEIPASS + '\\img\system_help.ico')
	except Exception:
				try:
					help_window.iconbitmap('C:\Users\Florian\Desktop\img\system_help.ico')
				except Exception:
					pass
	
	#img1 = PhotoImage(file="C:\Users\Florian\Desktop\img\h_f_1.gif")
	img1 = PhotoImage(file=sys._MEIPASS + '\\img\h_f_1.gif')
	w1 = tk.Label(help_window, image=img1)
	w1.image = img1 # keep a reference!
	w1.pack(side="right")
	#img2 = PhotoImage(file="C:\Users\Florian\Desktop\img\h_f_2.gif")
	img2 = PhotoImage(file=sys._MEIPASS + '\\img\h_f_2.gif')
	w2 = tk.Label(help_window, image=img2)
	w2.image = img2 # keep a reference!
	w2.pack(side="top")

	display1 = tk.Label(help_window, text="This App is a tool to create simple plots from csv-formatted files.\nThe tool is currently only suitable for csv-data formatted by the SG-Feinstaubboxen.\nYou can import your files via drag/drop or with the Filemanager. The usage is illustrated \nin the following pictures. For further help/information please refer to:")
	display1.pack()

	link1 = tk.Label(help_window, text="Website SG-Feinstaubboxen (https://github.com/Fbisinger/SG-Feinstaubboxen)", fg="blue", cursor="hand2")
	link1.pack()
	link1.bind("<Button-1>", lambda e: callback("https://github.com/Fbisinger/SG-Feinstaubboxen"))
	
	display2 = tk.Label(help_window, text="This help information is suitable for all versions up to v1.5\nFeinstaubboxen Schelztor-Gymnasium (c) 2020 F.Bisinger")
	display2.pack()

	#img3 = PhotoImage(file="C:\Users\Florian\Desktop\img\logo.gif")
	img3 = PhotoImage(file=sys._MEIPASS + '\\img\logo.gif')
	w3 = tk.Label(help_window, image=img3, cursor="hand2")
	w3.image = img3 # keep a reference!
	w3.pack()
	w3.bind("<Button-1>", lambda e: callback("https://www.schelztor-gymnasium.de/"))

def get_info():
	webbrowser.open('https://github.com/Fbisinger/SG-Feinstaubboxen', new=2)

def clear_cache_ask():
	if len(ID) > 0:
		if tkMessageBox.askyesno("Are you sure?","Will delete all cached Data!"):
			del time [:]
			del ID [:]
			del temp [:]
			del hum [:]
			del pm10 [:]
			del pm25 [:]
			del pmall [:]
			v.set("Browse File/drag-drop it here")
			progress_var.set(0)
			num_datasets = 0
			datasets_var.set("0 Datasets loaded")
	else:
		tkMessageBox.showwarning("No Data to clear!", "There is no cached Data to clear!")

def clear_cache():
		del time [:]
		del ID [:]
		del temp [:]
		del hum [:]
		del pm10 [:]
		del pm25 [:]
		del pmall [:]
		v.set("Browse File/drag-drop it here")
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
	
def open_file():
	global v
	global csv_file_path
	if len(ID) > 0:
		if(tkMessageBox.askyesno("You have already imported data!", "Do you want to override the\nexisting Data with new Data?")):
			clear_cache()
			csv_file_path.set(askopenfilename())
			if csv_file_path.get():
				print("File Path: " + csv_file_path.get())
				v.set(csv_file_path.get())
				import_csv_data()
	else:
		csv_file_path.set(askopenfilename())
		if csv_file_path.get():
			print("File Path: " + csv_file_path.get())
			v.set(csv_file_path.get())
			import_csv_data()

def drop(event):
	if len(ID) > 0:
		if(tkMessageBox.askyesno("You have already imported data!", "Do you want to override the\nexisting Data with new Data?")):
			clear_cache()
			csv_file_path.set(event.data)
			print("File Path: " + csv_file_path.get())
			v.set(csv_file_path.get())
			import_csv_data()
	else:
		csv_file_path.set(event.data)
		print("File Path: " + csv_file_path.get())
		v.set(csv_file_path.get())
		import_csv_data()

def import_csv_data():
	i = 0
	num_datasets = sum(1 for line in open(csv_file_path.get())) - 24
	print("Number of Datasets: " + str(num_datasets))
	pb["maximum"] = num_datasets

	with open(csv_file_path.get(), "r") as csvfile:
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

#root = Tkinter.Tk()
root = TkinterDnD.Tk()

root.title("Feinstaubboxen Schelztor-Gymnasium (c) 2020 F.Bisinger v1.5")
try:
	root.iconbitmap(sys._MEIPASS + '\\img\logo.ico')
except Exception:
            try:
				root.iconbitmap('C:\Users\Florian\Desktop\img\logo.ico')
            except Exception:
                pass
tk.Label(root, text='File Path').grid(row=0, column=0)
tk.Label(root, text='This Script, written and debugged \n in Python by Florian Bisinger \n is a tool to create simple plots \n from csv-files').grid(row=0, column=2)

csv_file_path = tk.StringVar()
v = tk.StringVar()
v.set("Browse File/drag-drop it here")
entry = tk.Entry(root, textvar=v)
entry.grid(row=0, column=1, ipadx=20, ipady=20)
entry.drop_target_register(DND_FILES)
entry.dnd_bind('<<Drop>>', drop)

#CheckVar = tk.IntVar()
#tk.Checkbutton(root, text = "disable progressbar", variable = CheckVar, onvalue = 1, offvalue = 0).grid(row=1, column=4)

tk.Button(root, text='Browse File',command=open_file, cursor="hand2").grid(row=1, column=0)
tk.Button(root, text='Generate Plot Temperature',command=plot_temp, cursor="hand2").grid(row=2, column=0)
tk.Button(root, text='Generate Plot Humidity',command=plot_hum, cursor="hand2").grid(row=2, column=1)
tk.Button(root, text='Generate Plot PM10',command=plot_pm10, cursor="hand2").grid(row=2, column=2)
tk.Button(root, text='Generate Plot PM2.5',command=plot_pm25, cursor="hand2").grid(row=2, column=3)
tk.Button(root, text='Generate Plot PMall',command=plot_pmall, cursor="hand2").grid(row=2, column=4)
tk.Button(root, text='Clear Cache',command=clear_cache_ask, cursor="hand2").grid(row=1, column=1)
tk.Button(root, text='About...',command=get_info, cursor="draft_small").grid(row=1, column=2)
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