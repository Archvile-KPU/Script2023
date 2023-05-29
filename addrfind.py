# -*- coding: utf-8 -*-
"""
Created on Mon May 29 22:16:48 2023

@author: MK
"""

import requests
import tkinter as tk
from tkinter import messagebox


def get_address():
    API_KEY = "YOUR_API_KEY"
    search = entry.get()
    url = f"http://www.juso.go.kr/addrlink/addrLinkApi.do?confmKey={API_KEY}&currentPage=1&countPerPage=1&keyword={search}&resultType=json"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data.get("results") and data["results"].get("juso"):
                roadAddr = data["results"]["juso"][0]["roadAddr"]
                jibunAddr = data["results"]["juso"][0].get("jibunAddr", "")
                messagebox.showinfo(title="Success", message=f"Road Address: {roadAddr}\nJibun Address: {jibunAddr}")
            else:
                messagebox.showerror(title="Error", message="No results found.")
        else:
            messagebox.showerror(title="Error", message="Failed to connect.")
    except Exception as e:
        messagebox.showerror(title="Error", message=str(e))


def clear_entry():
    entry.delete(0, tk.END)


root = tk.Tk()
root.geometry("300x200")
root.title("Address Finder")

label = tk.Label(root, text="Enter a search term:")
label.pack(pady=10)

entry = tk.Entry(root)
entry.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

search_button = tk.Button(button_frame, text="Search", command=get_address)
search_button.pack(side=tk.LEFT, padx=5)

clear_button = tk.Button(button_frame, text="Clear", command=clear_entry)
clear_button.pack(side=tk.LEFT, padx=5)

root.mainloop()