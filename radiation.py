import requests
import tkinter as tk

def get_radiation_level():
    selected_plant = power_plant.get()  # Get the selected power plant
    params = {'serviceKey': 'put_key_here', 'genName': selected_plant}
    url = 'http://data.khnp.co.kr/environ/service/realtime/radiorate'
    response = requests.get(url, params=params)
    radiation_data = response.content
    radiation_label.config(text="Radiation Level: {}".format(radiation_data))

window = tk.Tk()
window.title("Radiation Level at Nuclear Plants")

radiation_label = tk.Label(window, text="Radiation Level:")
radiation_label.pack()

# Create radio buttons for power plants
power_plant = tk.StringVar()
power_plant.set("WS")  # Set default selection to WS

radio_button_ws = tk.Radiobutton(window, text="월성", variable=power_plant, value="WS")
radio_button_ws.pack()

radio_button_kr = tk.Radiobutton(window, text="고리", variable=power_plant, value="KR")
radio_button_kr.pack()

radio_button_yk = tk.Radiobutton(window, text="한빛", variable=power_plant, value="YK")
radio_button_yk.pack()

radio_button_uj = tk.Radiobutton(window, text="한울", variable=power_plant, value="UJ")
radio_button_uj.pack()

radio_button_su = tk.Radiobutton(window, text="새울", variable=power_plant, value="SU")
radio_button_su.pack()

fetch_button = tk.Button(window, text="Fetch Radiation Level", command=get_radiation_level)
fetch_button.pack()

window.mainloop()