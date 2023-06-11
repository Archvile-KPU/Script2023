# -*- coding: utf-8 -*-
"""
Created on Tue May 30 06:52:53 2023

@author: MK
"""
import folium
import requests
import tkinter as tk
import threading
from tkinter import ttk
import openai
import telepot
import sys
from tkinter import messagebox
from cefpython3 import cefpython as cef
import xml.etree.ElementTree as ET
from PIL import Image, ImageTk
import tkinter.font



width = 300
height = 300

image = Image.open("sign.png")
emergency = Image.open("emergency.png")
warning = Image.open("warning.png")
attention = Image.open("attention.png")
safe = Image.open("safe.png")

image = image.resize((width, height))
emergency = emergency.resize((width, height))
warning = warning.resize((width, height))
attention = attention.resize((width, height))
safe = safe.resize((width, height))

global testnum
testnum = 0

# Set your OpenAI API key
openai.api_key = "YOUR_KEY"
API_KEY = 'key'
CHAT_ID = 'id'
BOT_ID = 'id'
def showMap(frame):
    global browser
    sys.excepthook = cef.ExceptHook
    window_info = cef.WindowInfo(frame.winfo_id())
    window_info.SetAsChild(frame.winfo_id(), [0,0,800,600])
    cef.Initialize()
    browser = cef.CreateBrowserSync(window_info, url='file:///map.html')
    cef.MessageLoop()


def setup():
    # 지도 저장
    # 위도 경도 지정
    m = folium.Map(location=[35.71385822435067, 129.47484965310252], zoom_start=13)
    # 마커 지정
    folium.Marker([35.71385822435067, 129.47484965310252], popup='월성').add_to(m)
    # html 파일로 저장
    m.save('map.html')

    # 브라우저를 위한 쓰레드 생성
    thread = threading.Thread(target=showMap, args=(frame2,))
    thread.daemon = True
    thread.start()

def pressed_1():
    m = folium.Map(location=[35.71385822435067, 129.47484965310252 ], zoom_start=13)
    folium.Marker([35.71385822435067, 129.47484965310252], popup='월성').add_to(m)
    m.save('map.html')
    browser.Reload()

def pressed_2():
    m = folium.Map(location=[35.321954256925586,129.29451805278634], zoom_start=13)
    folium.Marker([35.321954256925586,129.29451805278634], popup='고리').add_to(m)
    m.save('map.html')
    browser.Reload()

def pressed_3():
    m = folium.Map(location=[35.40912239274478,126.41475741340308], zoom_start=13)
    folium.Marker([35.40912239274478,126.41475741340308], popup='한빛').add_to(m)
    m.save('map.html')
    browser.Reload()

def pressed_4():
    m = folium.Map(location=[37.08605674376176,129.388632445903], zoom_start=13)
    folium.Marker([37.08605674376176,129.388632445903], popup='한울').add_to(m)
    m.save('map.html')
    browser.Reload()

def pressed_5():
    m = folium.Map(location=[35.33796053363176,129.31350573077788], zoom_start=13)
    folium.Marker([35.33796053363176,129.31350573077788], popup='새울').add_to(m)
    m.save('map.html')
    browser.Reload()
    
def get_radiation_level():
    selected_plant = power_plant.get()  # Get the selected power plant
    params = {'serviceKey': API_KEY, 'genName': selected_plant}
    url = 'http://data.khnp.co.kr/environ/service/realtime/radiorate'
    response = requests.get(url, params=params)
    
    #print(response.text)
    root = ET.fromstring(response.text)
    
    data_list = []  # List to store data points

    for item in root.iter("item"):
        expl = item.findtext("expl")
        name = item.findtext("name")
        value = item.findtext("value")
        data_list.append((name, expl, value))  # Append data points to the list

    # Display the fetched data
    radiobutton_label.config(text="Select a power plant: {}".format(selected_plant))

    if len(data_list) > 0:
        # Retrieve the first data point from the list
        name, expl, value = data_list[0]
        radiation_label.config(text="Radiation Level: {}usv/h".format(value))
        plant_label.config(text="Power Site: {}".format(name))
        powersite_label.config(text="Power Site expl: {}".format(expl))
    else:
        # No data points found
        radiation_label.config(text="Radiation Level: N/A")
        plant_label.config(text="Power Site: N/A")
        powersite_label.config(text="Power Site expl: N/A")
    
    # emergency
    if eval(value) > 0.973:
        print('emergency')
        image_e = ImageTk.PhotoImage(emergency)
        image_label.configure(image=image_e)
        image_label.image = image_e
        
        bot = telepot.Bot(BOT_ID)
        bot.sendMessage(CHAT_ID, "EMERGENCY. EVACUATE IMMEDIATELY")
        
    # warning
    elif eval(value) > 0.973:
        print('warning')
        image_w = ImageTk.PhotoImage(warning)
        image_label.configure(image=image_w)
        image_label.image = image_w
        
        bot = telepot.Bot(BOT_ID)
        bot.sendMessage(CHAT_ID, "Warning. Current level is dangerous.")
        
    # attention
    elif eval(value) > 0.12:
        print('attention')
        image_a = ImageTk.PhotoImage(attention)
        image_label.configure(image=image_a)
        image_label.image = image_a
        
        bot = telepot.Bot(BOT_ID)
        bot.sendMessage(CHAT_ID, "Current level needs attention.")
        
    # safe
    else:
        print('safe')
        image_s = ImageTk.PhotoImage(safe)
        image_label.configure(image=image_s)
        image_label.image = image_s
        
        bot = telepot.Bot(BOT_ID)
        bot.sendMessage(CHAT_ID, "Current level is safe.")

def testdrive(value):
    
    # emergency
    if value > 2:
        print('emergency')
        image_e = ImageTk.PhotoImage(emergency)
        image_label.configure(image=image_e)
        image_label.image = image_e
        
        radiation_label.config(text="Radiation Level: 999.999usv/h")
        plant_label.config(text="Power Site: N/A")
        powersite_label.config(text="Power Site expl: N/A")
        
        bot = telepot.Bot(BOT_ID)
        bot.sendMessage(CHAT_ID, "EMERGENCY. EVACUATE IMMEDIATELY")
        
    # warning
    elif value > 1:
        print('warning')
        image_w = ImageTk.PhotoImage(warning)
        image_label.configure(image=image_w)
        image_label.image = image_w
        
        radiation_label.config(text="Radiation Level: 0.973usv/h")
        plant_label.config(text="Power Site: N/A")
        powersite_label.config(text="Power Site expl: N/A")
        
        bot = telepot.Bot(BOT_ID)
        bot.sendMessage(CHAT_ID, "Warning. Current level is dangerous.")
        
    # attention
    elif value > 0:
        print('attention')
        image_a = ImageTk.PhotoImage(attention)
        image_label.configure(image=image_a)
        image_label.image = image_a
        
        radiation_label.config(text="Radiation Level: 0.121usv/h")
        plant_label.config(text="Power Site: N/A")
        powersite_label.config(text="Power Site expl: N/A")
        
        bot = telepot.Bot(BOT_ID)
        bot.sendMessage(CHAT_ID, "Current level needs attention.")
        
    # safe
    else:
        print('safe')
        image_s = ImageTk.PhotoImage(safe)
        image_label.configure(image=image_s)
        image_label.image = image_s
        
        radiation_label.config(text="Radiation Level: 0.000usv/h")
        plant_label.config(text="Power Site: N/A")
        powersite_label.config(text="Power Site expl: N/A")
        
        bot = telepot.Bot(BOT_ID)
        bot.sendMessage(CHAT_ID, "Current level is safe.")

def testpilot():
    global testnum
    testdrive(testnum)
    testnum += 1
    

def return_radiation_level(powersite):
    params = {'serviceKey': API_KEY, 'genName': powersite}
    url = 'http://data.khnp.co.kr/environ/service/realtime/radiorate'
    response = requests.get(url, params=params)

    #print(response.text)
    root = ET.fromstring(response.text)
    
    data_list = []  # List to store data points

    for item in root.iter("item"):
        expl = item.findtext("expl")
        name = item.findtext("name")
        value = item.findtext("value")
        data_list.append((name, expl, value))  # Append data points to the list

    if len(data_list) > 0:
        # Retrieve the first data point from the list
        name, expl, value = data_list[0]
    
    return value

def send_message():
    user_input = input_box.get("1.0", tk.END).strip()
    input_box.delete("1.0", tk.END)

    chatbox.config(state=tk.NORMAL)
    chatbox.insert(tk.END, "You: " + user_input + "\n\n")
    chatbox.config(state=tk.DISABLED)
    chatbox.see(tk.END)

    # Display "Generating response..." message
    chatbox.config(state=tk.NORMAL)
    chatbox.insert(tk.END, "ChatGPT: Generating response...\n\n")
    chatbox.config(state=tk.DISABLED)
    chatbox.see(tk.END)

    # Send user input to ChatGPT API as a prompt in a separate thread
    threading.Thread(target=generate_response, args=(user_input,)).start()


def generate_response(user_input):
    # Send user input to ChatGPT API as a prompt
    prompt = "You are a safety advisor.\nUser: " + user_input + "\nAssistant:"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1000  # Increase max_tokens for a longer response
    )
    bot_response = response.choices[0].text.strip()

    # Remove the "Generating response..." message
    chatbox.config(state=tk.NORMAL)
    chatbox.delete("end-3l", tk.END)
    chatbox.config(state=tk.DISABLED)

    # Update chatbox with the generated response
    chatbox.config(state=tk.NORMAL)
    chatbox.insert(tk.END, "ChatGPT: " + bot_response + "\n\n")
    chatbox.config(state=tk.DISABLED)
    chatbox.see(tk.END)
    bot = telepot.Bot('5875225809:AAF2gMF-bz1TzIQhQ7tqMu6su6H4FFjLzHQ')
    bot.sendMessage('6177831500', bot_response)


window = tk.Tk()
window.title("Radiation Level at Nuclear Plants")
window.geometry("1280x720")



# Create a notebook (tabbed interface)
notebook = ttk.Notebook(window, width=800, height=600)

# Create tabs
tab_radiobuttons = ttk.Frame(notebook)
tab_graph = ttk.Frame(notebook)
tab_maps = ttk.Frame(notebook)
tab_safety = ttk.Frame(notebook)
tab_telegram = ttk.Frame(notebook)

notebook.add(tab_radiobuttons, text="Radiation Level")
notebook.add(tab_graph, text="Graph")
notebook.add(tab_maps, text="Maps")
notebook.add(tab_safety, text="Safety")
notebook.add(tab_telegram, text="Others")

notebook.pack()

# Content for the Radiobuttons tab (tab_radiobuttons)

font=tk.font.Font(family="times new roman", size=20)
font2=tk.font.Font(size=15)


radiobutton_label = tk.Label(tab_radiobuttons, text="Select a power plant:", font=font)
radiobutton_label.pack(anchor="w")

plant_label = tk.Label(tab_radiobuttons, text="Power Site:", font=font)
plant_label.pack(anchor="w")

powersite_label = tk.Label(tab_radiobuttons, text="Power Site expl:", font=font)
powersite_label.pack(anchor="w")

radiation_label = tk.Label(tab_radiobuttons, text="Radiation Level:", font=font)
radiation_label.pack(anchor="w")

# Create radio buttons for power plants
power_plant = tk.StringVar()
power_plant.set("WS")  # Set default selection to WS

radio_button_ws = tk.Radiobutton(tab_radiobuttons, text="월성", variable=power_plant, value="WS", font=font2)
radio_button_ws.pack(anchor="w")

radio_button_kr = tk.Radiobutton(tab_radiobuttons, text="고리", variable=power_plant, value="KR", font=font2)
radio_button_kr.pack(anchor="w")

radio_button_yk = tk.Radiobutton(tab_radiobuttons, text="한빛", variable=power_plant, value="YK", font=font2)
radio_button_yk.pack(anchor="w")

radio_button_uj = tk.Radiobutton(tab_radiobuttons, text="한울", variable=power_plant, value="UJ", font=font2)
radio_button_uj.pack(anchor="w")

radio_button_su = tk.Radiobutton(tab_radiobuttons, text="새울", variable=power_plant, value="SU", font=font2)
radio_button_su.pack(anchor="w")

fetch_button = tk.Button(tab_radiobuttons, text="Fetch Radiation Level", command=get_radiation_level, font=font2)
fetch_button.pack(anchor="w")


test_button = tk.Button(tab_radiobuttons, text="Drill", command=testpilot, font=font2)
test_button.pack(anchor="s")

image_tk = ImageTk.PhotoImage(image)
image_label = tk.Label(tab_radiobuttons, image=image_tk)
image_label.place(x=500,y=0)


# Content for the Graph tab (tab_graph)
graph_label = tk.Label(tab_graph, text="Graph for all plants")
graph_label.pack()
height=600
width=800

return_radiation_level("WS")

fclist = ['월성','고리','한빛','한울','새울']
radlist = [eval(return_radiation_level("WS")),eval(return_radiation_level("KR")),eval(return_radiation_level("YK")),eval(return_radiation_level("UJ")),eval(return_radiation_level("SU"))]

canvas = tk.Canvas(graph_label,width=width,height=height)
canvas.pack()

histogram = [0 for _ in range(5)]
for i in range(5):
    histogram[i] += radlist[i]
canvas.create_line(10,height-100,width-10,height-100,tags='histogram')
barwidth = (width-20)/5
maxcount = max(histogram)
index=0
for i in range(5):
    canvas.create_text(10+i*barwidth+(barwidth/2),height-20,text=fclist[index],tags='histogram', font=font2)
    index+=1
    canvas.create_rectangle(10+i*barwidth,height-(height-100)*histogram[i]/maxcount,10+(i+1)*barwidth,height-100,tags='histogram', fill="green")
    canvas.create_text(10+i*barwidth+(barwidth/2),height-(height-50)*histogram[i]/maxcount,text=str(histogram[i]),tags='histogram', font=font2)

# Maps tab

frame1 = tk.Frame(tab_maps)
frame1.pack(side=tk.LEFT)
tk.Button(frame1, text='월성', command=pressed_1, font=font2).pack()
tk.Button(frame1, text='고리', command=pressed_2, font=font2).pack()
tk.Button(frame1, text='한빛', command=pressed_3, font=font2).pack()
tk.Button(frame1, text='한울', command=pressed_4, font=font2).pack()
tk.Button(frame1, text='새울', command=pressed_5, font=font2).pack()
frame2 = tk.Frame(tab_maps, width=800, height=600)
frame2.pack(side=tk.LEFT)
setup()

#chatGPT module

chatbox = tk.Text(tab_safety, bd=1, relief=tk.SOLID, height="8", width="50")
chatbox.config(state=tk.DISABLED)
chatbox.place(x=6, y=6, height=385, width=480)

# Create user input box
input_box = tk.Text(tab_safety, bd=0, bg="white", height="4", width="30")
input_box.place(x=128, y=400, height=88, width=348)

# Create send button
send_button = tk.Button(tab_safety, text="Send", command=send_message, height=5, width=12, font=font2)
send_button.place(x=6, y=400, height=88, width=120)

window.mainloop()
