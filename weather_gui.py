import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from io import BytesIO
import random

API_KEY = "a614e7bc9c3120a512f68345d09c196c"

def on_entry_click(event):
    if city_entry.get() == "Enter City":
        city_entry.delete(0, tk.END)
        city_entry.config(fg="white")


def on_focusout(event):
    if city_entry.get() == "":
        city_entry.insert(0, "Enter City")
        city_entry.config(fg="gray")

def get_weather():

    city = city_entry.get().strip()

    if city == "" or city == "Enter City":
        messagebox.showwarning(
            "Missing City",
            "Please enter a city name 🌍"
        )
        return

    result_label.config(text="Loading weather... ⏳")

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    try:

        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:

            temperature = data["main"]["temp"]
            weather = data["weather"][0]["description"].title()
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]

            # Weather icon
            icon_code = data["weather"][0]["icon"]

            icon_url = f"http://openweathermap.org/img/wn/{icon_code}@4x.png"

            icon_response = requests.get(icon_url)

            icon_image = Image.open(BytesIO(icon_response.content))

            icon_photo = ImageTk.PhotoImage(icon_image)

            weather_icon_label.config(image=icon_photo)
            weather_icon_label.image = icon_photo

            result_label.config(
                text=f"""
📍 {city}

🌡 {temperature}°C
☁ {weather}

💧 Humidity: {humidity}%
🌬 Wind Speed: {wind_speed} m/s
"""
            )

        else:
            messagebox.showerror(
                "City Not Found",
                "Couldn't find that city 😢"
            )

    except:
        messagebox.showerror(
            "Connection Error",
            "Check your internet connection 🌐"
        )


    if city == "" or city == "Enter City":
        messagebox.showwarning("Warning", "Please enter a city name")
        return

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:

        temperature = data["main"]["temp"]
        weather = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        # Weather icon
        icon_code = data["weather"][0]["icon"]

        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"

        icon_response = requests.get(icon_url)

        icon_image = Image.open(BytesIO(icon_response.content))

        icon_photo = ImageTk.PhotoImage(icon_image)

        weather_icon_label.config(image=icon_photo)
        weather_icon_label.image = icon_photo

        result_label.config(
            text=f"""
📍 City: {city}

🌡 Temperature: {temperature}°C

☁ Weather: {weather}

💧 Humidity: {humidity}%

🌬 Wind Speed: {wind_speed} m/s
"""
        )

    else:
        messagebox.showerror("Error", "City not found or API issue")


# ---------------- WINDOW ---------------- #

root = tk.Tk()
root.title("Modern Weather App")
root.geometry("700x650")
root.configure(bg="#0f172a")
root.resizable(False, False)

canvas = tk.Canvas(
    root,
    width=700,
    height=650,
    bg="#0f172a",
    highlightthickness=0
)

canvas.place(x=0, y=0)

# ---------------- RAIN ANIMATION ---------------- #

raindrops = []


def create_rain():
    for i in range(120):

        x = random.randint(0, 700)
        y = random.randint(0, 650)

        drop = canvas.create_line(
            x,
            y,
            x + 2,
            y + 12,
            fill="#7dd3fc",
            width=2
        )

        raindrops.append(drop)


def animate_rain():

    for drop in raindrops:

        canvas.move(drop, -1, 10)

        coords = canvas.coords(drop)

        if coords[1] > 650:

            x = random.randint(0, 700)

            canvas.coords(
                drop,
                x,
                0,
                x + 2,
                12
            )

    root.after(50, animate_rain)


create_rain()
animate_rain()

# ---------------- UI ---------------- #

title_label = tk.Label(
    root,
    text="🌧 Modern Weather App",
    font=("Arial", 26, "bold"),
    bg="#0f172a",
    fg="white"
)

title_label.place(relx=0.5, y=50, anchor="center")

city_entry = tk.Entry(
    root,
    font=("Segoe UI", 16),
    width=24,
    bg="#1e293b",
    fg="white",
    insertbackground="white",
    relief="flat",
    justify="center",
    bd=0
)
city_entry.place(relx=0.5, y=140, anchor="center", height=45)

city_entry.insert(0, "Enter City")
city_entry.config(fg="gray")
city_entry.bind("<FocusIn>", on_entry_click)
city_entry.bind("<FocusOut>", on_focusout)

search_button = tk.Button(
    root,
    text="Search Weather",
    font=("Segoe UI", 13, "bold"),
    bg="#38bdf8",
    fg="white",
    activebackground="#0ea5e9",
    activeforeground="white",
    relief="flat",
    padx=25,
    pady=10,
    cursor="hand2",
    command=get_weather
)

search_button.place(relx=0.5, y=200, anchor="center")

# Weather Icon
weather_icon_label = tk.Label(
    root,
    bg="#0f172a"
)

weather_icon_label.place(relx=0.5, y=300, anchor="center")

# Result
result_label = tk.Label(
    root,
    text="",
    font=("Arial", 15),
    bg="#0f172a",
    fg="white",
    justify="left"
)

result_label.place(relx=0.5, y=500, anchor="center")

root.mainloop()
root.bind("<Return>", lambda event: get_weather())