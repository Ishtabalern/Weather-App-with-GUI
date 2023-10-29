import requests
import pytz
import pyqrcode
from pyqrcode import QRCode
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

def get_weather(city, api_key, timezone):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if data["cod"] == 200:
        main_data = data["main"]
        weather_data = data["weather"][0]

        temperature = main_data["temp"]
        description = weather_data["description"]

        current_time = datetime.now(pytz.timezone(timezone))

        weather_info = f"Weather in {city}:\n"
        weather_info += f"Temperature: {temperature}°C\n"
        weather_info += f"Description: {description.capitalize()}\n"
        weather_info += f"Current Time: {current_time.strftime('%Y-%m-%d %H:%M:%S')} ({timezone})"

        qr = pyqrcode.create(weather_info)
        qr.png("weather_qr.png", scale=6)

        qr_image = Image.open("weather_qr.png")
        qr_image = qr_image.resize((200, 200))
        qr_photo = ImageTk.PhotoImage(qr_image)

        qr_label = tk.Label(window, image=qr_photo)
        qr_label.photo = qr_photo
        qr_label.pack()
    else:
        messagebox.showerror("Error", f"Could not fetch weather data for {city}. Error code: {data['cod']}")

def get_weather_from_gui():
    api_key = "3301007ff78e08c345eeba4bc785d345"
    city = city_entry.get()
    continent = continent_entry.get()
    timezone = str(continent + "/" + city)
    get_weather(city, api_key, timezone)

# Create a GUI window
window = tk.Tk()
window.title("Weather App")

# Create and place labels and entry fields
continent_label = tk.Label(window, text="Continent:")
continent_label.pack()
continent_entry = tk.Entry(window)
continent_entry.pack()

city_label = tk.Label(window, text="City:")
city_label.pack()
city_entry = tk.Entry(window)
city_entry.pack()

# Create a button to fetch weather
fetch_button = tk.Button(window, text="Get Weather", command=get_weather_from_gui)
fetch_button.pack()

# Start the GUI event loop
window.mainloop()
