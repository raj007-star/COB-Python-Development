import requests
import tkinter as tk
from tkinter import Label, Entry, Button, PhotoImage
from PIL import Image, ImageTk

def get_weather_data(api_key, city):
    base_url = "http://api.openweathermap.org/data/2.5/forecast"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }
    response = requests.get(base_url, params=params)
    return response.json()

def display_weather_data():
    city = city_entry.get()
    weather_data = get_weather_data(api_key, city)

    if "cod" in weather_data and weather_data["cod"] == "200":
        display_forecast(weather_data)
    else:
        result_label.config(text="City not found or an error occurred.")

def display_forecast(data):
    result_label.config(text=f"Weather in {data['city']['name']}, {data['city']['country']}:")
    forecast = data['list']
    for i in range(5):  # Display a 5-day forecast
        day_data = forecast[i * 8]  # Data for every 24 hours
        temp = day_data['main']['temp']
        description = day_data['weather'][0]['description']
        icon_id = day_data['weather'][0]['icon']
        icon_url = f"http://openweathermap.org/img/w/{icon_id}.png"

        # Display the date, temperature, description, and weather icon for each day
        date_label[i].config(text=day_data['dt_txt'].split()[0])
        temp_label[i].config(text=f"Temp: {temp}°C")
        desc_label[i].config(text=f"Description: {description}")
        icon = Image.open(requests.get(icon_url, stream=True).raw)
        icon = ImageTk.PhotoImage(icon)
        icon_label[i].config(image=icon)
        icon_label[i].image = icon

api_key = 'YOUR_API_KEY'  # Replace with your OpenWeatherMap API key

app = tk.Tk()
app.title("5-Day Weather Forecast")

city_label = Label(app, text="Enter city name:")
city_label.pack()

city_entry = Entry(app)
city_entry.pack()

search_button = Button(app, text="Search", command=display_weather_data)
search_button.pack()

result_label = Label(app, text="")
result_label.pack()

# Create labels and icons for each day
date_label = []
temp_label = []
desc_label = []
icon_label = []

for i in range(5):
    date_label.append(Label(app, text=""))
    temp_label.append(Label(app, text=""))
    desc_label.append(Label(app, text=""))
    icon_label.append(Label(app, image=None))
    
    date_label[i].pack()
    temp_label[i].pack()
    desc_label[i].pack()
    icon_label[i].pack()

app.mainloop()
