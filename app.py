from flask import Flask, render_template, jsonify
import requests
from datetime import datetime, timezone, timedelta
import webbrowser
from threading import Timer
import os

app = Flask(__name__)

# --- Настройки ---
API_KEY = 'efd12ce859284731dc0b5dded9513bae'
URL = 'https://api.openweathermap.org/data/2.5/weather'
LAT = 55.9177
LON = 37.7274

# Часовой пояс UTC+3 (Москва)
TZ_OFFSET = timezone(timedelta(hours=3))

# --- Направление ветра ---
def get_wind_direction(deg):
    directions = ['Север', 'Северо-восток', 'Восток', 'Юго-восток',
                  'Юг', 'Юго-запад', 'Запад', 'Северо-запад']
    return directions[round(deg / 45) % 8]

# --- Маршрут: главная страница ---
@app.route('/')
def index():
    return render_template('index.html')

# --- API: получение погоды ---
@app.route('/api/weather')
def weather_api():
    try:
        response = requests.get(URL, params={
            'lat': LAT,
            'lon': LON,
            'appid': API_KEY,
            'units': 'metric',
            'lang': 'ru'
        }).json()

        city = response['name']
        desc = response['weather'][0]['description'].capitalize()
        icon = response['weather'][0]['icon']
        temp = round(response['main']['temp'], 1)
        feels_like = round(response['main']['feels_like'], 1)
        humidity = response['main']['humidity']
        pressure_mmhg = round(response['main']['pressure'] * 0.75)
        wind_speed = response['wind']['speed']
        wind_dir = get_wind_direction(response['wind']['deg'])

        # Конвертируем Unix timestamp в UTC+3
        sunrise_utc = datetime.fromtimestamp(response['sys']['sunrise'], tz=timezone.utc)
        sunset_utc = datetime.fromtimestamp(response['sys']['sunset'], tz=timezone.utc)

        sunrise_local = sunrise_utc.astimezone(TZ_OFFSET).strftime('%H:%M')
        sunset_local = sunset_utc.astimezone(TZ_OFFSET).strftime('%H:%M')

        return jsonify({
            "city": city,
            "desc": desc,
            "icon": icon,
            "temp": temp,
            "feels_like": feels_like,
            "humidity": humidity,
            "pressure": pressure_mmhg,
            "wind": f"{wind_speed} м/с, {wind_dir}",
            "sunrise": sunrise_local,
            "sunset": sunset_local
        })
    except Exception as e:
        print("Ошибка:", e)
        return jsonify({"error": "Не удалось получить данные"}), 500

# Функция для автоматического открытия браузера
def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000')

if __name__ == '__main__':
    # Явно удаляем FLASK_APP из окружения, чтобы избежать reloader
    os.environ.pop('FLASK_APP', None)
    print("✅ Сервер запущен. PID:", os.getpid())

    # Просто запускаем браузер один раз — без проверки WERKZEUG_RUN_MAIN
    # Потому что use_reloader=False → только один процесс
    Timer(1, open_browser).start()

    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False,
        use_reloader=False  # гарантируем один процесс
    )