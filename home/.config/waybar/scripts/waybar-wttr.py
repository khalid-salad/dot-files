#!/usr/bin/env python

import json
import requests
from datetime import datetime

WEATHER_CODES = {
    "113": "☀️",
    "116": "⛅️",
    "119": "☁️",
    "122": "☁️",
    "143": "🌫",
    "176": "🌦",
    "179": "🌧",
    "182": "🌧",
    "185": "🌧",
    "200": "⛈",
    "227": "🌨",
    "230": "❄️",
    "248": "🌫",
    "260": "🌫",
    "263": "🌦",
    "266": "🌦",
    "281": "🌧",
    "284": "🌧",
    "293": "🌦",
    "296": "🌦",
    "299": "🌧",
    "302": "🌧",
    "305": "🌧",
    "308": "🌧",
    "311": "🌧",
    "314": "🌧",
    "317": "🌧",
    "320": "🌨",
    "323": "🌨",
    "326": "🌨",
    "329": "❄️",
    "332": "❄️",
    "335": "❄️",
    "338": "❄️",
    "350": "🌧",
    "353": "🌦",
    "356": "🌧",
    "359": "🌧",
    "362": "🌧",
    "365": "🌧",
    "368": "🌨",
    "371": "❄️",
    "374": "🌧",
    "377": "🌧",
    "386": "⛈",
    "389": "🌩",
    "392": "⛈",
    "395": "❄️",
}

data = {}


weather = requests.get("https://wttr.in/Houston?format=j1").json()


def format_time(time):
    time = int(time) // 100
    if time < 12:
        ampm = "AM"
        if time == 0:
            return "Midnight".zfill(2)
    else:
        time -= 12
        ampm = "PM"
        if time == 0:
            return "Noon".zfill(2)
    return f"{time} {ampm}".zfill(2)


def format_temp(hour):
    c_temp = hour["FeelsLikeC"]
    f_temp = hour["FeelsLikeF"]
    return f"{f_temp}°F / {c_temp}°C".ljust(3)


def format_chances(hour):
    chances = {
        "chanceoffog": "Fog",
        "chanceoffrost": "Frost",
        "chanceofovercast": "Overcast",
        "chanceofrain": "Rain",
        "chanceofsnow": "Snow",
        "chanceofsunshine": "Sunshine",
        "chanceofthunder": "Thunder",
        "chanceofwindy": "Wind",
    }

    conditions = []
    for event, name in chances.items():
        likelihood = hour[event]
        if int(likelihood) > 0:
            conditions.append(f"{name} {likelihood}%")
    return ", ".join(conditions)


def main():
    weather_code = WEATHER_CODES[weather["current_condition"][0]["weatherCode"]]
    weather_c = weather["current_condition"][0]["FeelsLikeC"]
    weather_f = weather["current_condition"][0]["FeelsLikeF"]
    data["text"] = f"{weather_code}  {weather_f}°F / {weather_c}°C"

    current_condition = weather['current_condition'][0]
    weather_code = current_condition['weatherDesc'][0]['value']
    weather_c = current_condition['temp_C']
    weather_f = current_condition['temp_F']
    feels_like_c = current_condition['FeelsLikeC']
    feels_like_f = current_condition['FeelsLikeF']
    wind_speed_kmph = current_condition['windspeedKmph']
    wind_speed_miph = current_condition['windspeedMiles']
    humidity = current_condition['humidity']
     
    data["tooltip"] = f"""<b>{weather_code} {weather_c}°</b>
Feels like: {feels_like_f}°F / {feels_like_c}°C
Wind: {wind_speed_miph} mph / {wind_speed_kmph} kmph
Humidity: {humidity}%
"""
    for i, day in enumerate(weather["weather"]):
        if i == 0:
            relative_day = "Today, "
        elif i == 1:
            relative_day = "Tomorrow, "
        else:
            relative_day = ""
        date = day['date']
        hi_c = day['maxtempC']
        lo_c = day['mintempC']
        hi_f = day['maxtempF']
        lo_f = day['mintempF']
        data["tooltip"] += f"<b>{relative_day}{date}"
        data["tooltip"] += f"{date}</b>\n"
        data["tooltip"] += f"⬆️ {hi_f}°F / {hi_c}°C ⬇️ {lo_f}°F / {lo_c}°C "
        data[
            "tooltip"
        ] += f"🌅 {day['astronomy'][0]['sunrise']} 🌇 {day['astronomy'][0]['sunset']}\n"
        for hour in day["hourly"]:
            time = hour['time']
            formatted_time = format_time(time)
            if i == 0 and int(time) < datetime.now().hour - 2: 
                continue
            data[
                "tooltip"
            ] += f"{format_time(hour['time'])} {WEATHER_CODES[hour['weatherCode']]} {format_temp(hour)} {hour['weatherDesc'][0]['value']}, {format_chances(hour)}\n"

    print(json.dumps(data))


if __name__ == "__main__":
    main()
