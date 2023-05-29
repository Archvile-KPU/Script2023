import requests
import tkinter as tk

def get_radiation_level():
    url = 'http://data.khnp.co.kr/environ/service/realtime/radiorate'
    params = {'serviceKey': 'put_key_here', 'genName': 'put_gen_name_here'}
    response = requests.get(url, params=params)
    radiation_data = response.content
    radiation_label.config(text="Radiation Level: {}".format(radiation_data))

window = tk.Tk()
window.title("Radiation Level at Nuclear Plants")

radiation_label = tk.Label(window, text="Radiation Level:")
radiation_label.pack()

fetch_button = tk.Button(window, text="Fetch Radiation Level", command=get_radiation_level)
fetch_button.pack()

window.mainloop()