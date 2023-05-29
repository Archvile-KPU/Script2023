# -*- coding: utf-8 -*-
"""
Created on Tue May 30 06:24:54 2023

@author: MK
"""

import requests
import tkinter as tk
from tkinter import ttk

def get_radiation_level():
    selected_plant = power_plant.get()  # Get the selected power plant
    params = {'serviceKey': 'put_key_here', 'genName': selected_plant}
    url = 'http://data.khnp.co.kr/environ/service/realtime/radiorate'
    response = requests.get(url, params=params)
    radiation_data = response.content
    radiation_label.config(text="Radiation Level: {}".format(radiation_data))

window = tk.Tk()
window.title("Radiation Level at Nuclear Plants")



# Create a notebook (tabbed interface)
notebook = ttk.Notebook(window)

# Create tabs
tab_radiobuttons = ttk.Frame(notebook)
tab_blank = ttk.Frame(notebook)

notebook.add(tab_radiobuttons, text="Radiobuttons")
notebook.add(tab_blank, text="Blank")

notebook.pack()

# Content for the Radiobuttons tab (tab_radiobuttons)
radiobutton_label = tk.Label(tab_radiobuttons, text="Select a power plant:")
radiobutton_label.pack()

radiation_label = tk.Label(tab_radiobuttons, text="Radiation Level:")
radiation_label.pack()

# Create radio buttons for power plants
power_plant = tk.StringVar()
power_plant.set("WS")  # Set default selection to WS

radio_button_ws = tk.Radiobutton(tab_radiobuttons, text="월성", variable=power_plant, value="WS")
radio_button_ws.pack()

radio_button_kr = tk.Radiobutton(tab_radiobuttons, text="고리", variable=power_plant, value="KR")
radio_button_kr.pack()

radio_button_yk = tk.Radiobutton(tab_radiobuttons, text="한빛", variable=power_plant, value="YK")
radio_button_yk.pack()

radio_button_uj = tk.Radiobutton(tab_radiobuttons, text="한울", variable=power_plant, value="UJ")
radio_button_uj.pack()

radio_button_su = tk.Radiobutton(tab_radiobuttons, text="새울", variable=power_plant, value="SU")
radio_button_su.pack()

fetch_button = tk.Button(tab_radiobuttons, text="Fetch Radiation Level", command=get_radiation_level)
fetch_button.pack()

# Content for the Blank tab (tab_blank)
blank_label = tk.Label(tab_blank, text="This is a blank page.")
blank_label.pack()


height=400
width=600

fclist = ['월성','고리','한빛','한울','새울']
radlist = [40,56,99,0,30]

canvas = tk.Canvas(blank_label,width=width,height=height)
canvas.pack()

histogram = [0 for _ in range(5)]
#for _ in range(1000):
    #histogram[random.randint(0,4)] += 1
for i in range(5):
    histogram[i] += radlist[i]
canvas.create_line(10,height-10,width-10,height-10,tags='histogram')
barwidth = (width-20)/5
maxcount = max(histogram)
index=0
for i in range(5):
    canvas.create_text(10+i*barwidth+(barwidth/2),height-5,text=fclist[index],tags='histogram')
    index+=1
    canvas.create_rectangle(10+i*barwidth,height-(height-10)*histogram[i]/maxcount,10+(i+1)*barwidth,height-10,tags='histogram')
    canvas.create_text(10+i*barwidth+(barwidth/2),height-(height)*histogram[i]/maxcount,text=str(histogram[i]),tags='histogram')



window.mainloop()