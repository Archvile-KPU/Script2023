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

# Set your OpenAI API key
openai.api_key = "YOUR_KEY"

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
    m = folium.Map(location=[37.3402849, 126.7313189], zoom_start=13)
    # 마커 지정
    folium.Marker([37.3402849, 126.7313189], popup='한국산업기술대').add_to(m)
    # html 파일로 저장
    m.save('map.html')

    # 브라우저를 위한 쓰레드 생성
    thread = threading.Thread(target=showMap, args=(frame2,))
    thread.daemon = True
    thread.start()

def pressed_1():
    m = folium.Map(location=[37.3402849, 126.7313189], zoom_start=13)
    folium.Marker([37.3402849, 126.7313189], popup='한국산업기술대').add_to(m)
    m.save('map.html')
    browser.Reload()

def pressed_2():
    m = folium.Map(location=[37.4145018,126.6959112], zoom_start=13)
    folium.Marker([37.4145018,126.6959112], popup='서울대').add_to(m)
    m.save('map.html')
    browser.Reload()

def pressed_3():
    m = folium.Map(location=[37.5657882,126.936378], zoom_start=13)
    folium.Marker([37.5657882,126.936378], popup='연세대').add_to(m)
    m.save('map.html')
    browser.Reload()

def get_radiation_level():
    selected_plant = power_plant.get()  # Get the selected power plant
    params = {'serviceKey': 'YOUR_KEY', 'genName': selected_plant}
    url = 'http://data.khnp.co.kr/environ/service/realtime/radiorate'
    response = requests.get(url, params=params)
    radiation_data = response.content
    #radiation_data = 0.007
    radiation_label.config(text="Radiation Level: {}usv/h".format(radiation_data))

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


# Content for the Graph tab (tab_graph)
graph_label = tk.Label(tab_graph, text="Graph for all plants")
graph_label.pack()
height=600
width=800

fclist = ['월성','고리','한빛','한울','새울']
radlist = [0.093,0.110,0.099,0.109,0.094]

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
    canvas.create_text(10+i*barwidth+(barwidth/2),height-20,text=fclist[index],tags='histogram')
    index+=1
    canvas.create_rectangle(10+i*barwidth,height-(height-100)*histogram[i]/maxcount,10+(i+1)*barwidth,height-100,tags='histogram', fill="green")
    canvas.create_text(10+i*barwidth+(barwidth/2),height-(height-50)*histogram[i]/maxcount,text=str(histogram[i]),tags='histogram')

# Maps tab

frame1 = tk.Frame(tab_maps)
frame1.pack(side=tk.LEFT)
tk.Button(frame1, text='한국산업기술대', command=pressed_1).pack()
tk.Button(frame1, text='서울대', command=pressed_2).pack()
tk.Button(frame1, text='연세대', command=pressed_3).pack()
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
send_button = tk.Button(tab_safety, text="Send", command=send_message, height=5, width=12)
send_button.place(x=6, y=400, height=88, width=120)




'''
map_ws = folium.Map(location=[129.4757162, 35.713563], zoom_start=12)
map_kr = folium.Map(location=[129.4757162, 35.713563], zoom_start=12)
map_yk = folium.Map(location=[129.4757162, 35.713563], zoom_start=12)
map_uj = folium.Map(location=[129.4757162, 35.713563], zoom_start=12)
map_su = folium.Map(location=[129.4757162, 35.713563], zoom_start=12)

frame_ws = ttk.Frame(tab_maps)
frame_kr = ttk.Frame(tab_maps)
frame_yk = ttk.Frame(tab_maps)
frame_uj = ttk.Frame(tab_maps)
frame_su = ttk.Frame(tab_maps)

# Embed maps into frames
map_ws_frame = folium.IFrame(width=400, height=400)
map_ws_frame.add_child(map_ws)
map_ws_frame.grid(row=0, column=0, padx=10, pady=10)

map_kr_frame = folium.IFrame(width=400, height=400)
map_kr_frame.add_child(map_kr)
map_kr_frame.grid(row=0, column=1, padx=10, pady=10)

map_yk_frame = folium.IFrame(width=400, height=400)
map_yk_frame.add_child(map_yk)
map_yk_frame.grid(row=1, column=0, padx=10, pady=10)

map_uj_frame = folium.IFrame(width=400, height=400)
map_uj_frame.add_child(map_uj)
map_uj_frame.grid(row=1, column=1, padx=10, pady=10)

map_su_frame = folium.IFrame(width=400, height=400)
map_su_frame.add_child(map_su)
map_su_frame.grid(row=2, column=0, padx=10, pady=10)

frame_ws.pack()
frame_kr.pack()
frame_yk.pack()
frame_uj.pack()
frame_su.pack()

'''
window.mainloop()
