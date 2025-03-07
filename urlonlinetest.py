import requests
import socket
import time
import sys
import tkinter as tk

def check_dns():
    try:
        socket.create_connection(("1.1.1.1", 53), timeout=5)
        return True
    except (socket.timeout, socket.error):
        return False

def check_status_page():
    url = "https://pmartinasi.es/"
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False

def update_status():
    dns_status = check_dns()
    status_page = check_status_page()
    
    if dns_status and status_page:
        status_label.config(text="Cloudflare is ONLINE", fg="black")
        canvas.itemconfig(light, fill="green")
    elif dns_status or status_page:
        status_label.config(text="Cloudflare is PARTIALLY ONLINE", fg="black")
        canvas.itemconfig(light, fill="yellow")
    else:
        status_label.config(text="Cloudflare is OFFLINE", fg="black")
        canvas.itemconfig(light, fill="red")
    
    root.after(5000, update_status)

root = tk.Tk()
root.title("Site Status")
root.geometry("400x300")
root.configure(bg="white")

title_label = tk.Label(root, text="Cloudflare Status Checker", font=("Arial", 14, "bold"), bg="white", fg="black")
title_label.pack(pady=10)

canvas = tk.Canvas(root, width=100, height=100, bg="white", highlightthickness=0)
canvas.pack()
light = canvas.create_oval(25, 25, 75, 75, fill="gray")

status_label = tk.Label(root, text="Checking...", font=("Arial", 12), bg="white", fg="black")
status_label.pack(pady=10)

update_status()
root.mainloop()
