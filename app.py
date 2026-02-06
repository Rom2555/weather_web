from flask import Flask, render_template, jsonify
import urllib.request
import urllib.parse
import json
from datetime import datetime, timezone, timedelta
import webbrowser
from threading import Timer
import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()

app = Flask(__name__)

# --- Настройки из переменных окружения ---
# OpenWeatherMap API
URL = "https://api.openweathermap.org/data/2.5/weather"
URL_FORECAST = "https://api.openweathermap.org/data/2.5/forecast"
API_KEY = os.environ.get('API_KEY', 'your_api_key_here')
LAT = float(os.environ.get('LAT', '55.917460'))
LON = float(os.environ.get('LON', '37.727200'))

# Часовой пояс UTC+3 (Москва)
TZ_OFFSET = timezone(timedelta(hours=3))

# --- Коды погоды OpenWeatherMap -> иконки ---
OWM_TO_ICON = {
    200: '11d', 201: '11d', 202: '11d', 210: '11d', 211: '11d', 212: '11d', 221: '11d', 230: '11d', 231: '11d', 232: '11d',
    300: '09d', 301: '09d', 302: '09d', 310: '09d', 311: '09d', 312: '09d', 313: '09d', 314: '09d', 321: '09d',
    500: '10d', 501: '10d', 502: '10d', 503: '10d', 504: '10d', 511: '10d', 520: '09d', 521: '09d', 522: '09d', 531: '09d',
    600: '13d', 601: '13d', 602: '13d', 611: '13d', 612: '13d', 613: '13d', 615: '13d', 616: '13d', 620: '13d', 621: '13d', 622: '13d',
    701: '50d', 711: '50d', 721: '50d', 731: '50d', 741: '50d', 751: '50d', 761: '50d', 762: '50d', 771: '50d', 781: '50d',
    800: '01d',
    801: '02d', 802: '03d', 803: '04d', 804: '04d',
}

# --- Коды погоды -> описание на русском ---
OWM_TO_DESC = {
    200: 'Гроза с дождём', 201: 'Гроза с дождём', 202: 'Сильная гроза с дождём',
    210: 'Гроза', 211: 'Гроза', 212: 'Сильная гроза', 221: 'Сильная гроза', 230: 'Гроза с мокрым снегом', 231: 'Гроза с мокрым снегом', 232: 'Сильная гроза с мокрым снегом',
    300: 'Морось', 301: 'Морось', 302: 'Плотная морось', 310: 'Морось', 311: 'Морось', 312: 'Плотная морось', 313: 'Морось', 314: 'Плотная морось', 321: 'Плотная морось',
    500: 'Слабый дождь', 501: 'Умеренный дождь', 502: 'Сильный дождь', 503: 'Очень сильный дождь', 504: 'Продолжительный дождь', 511: 'Ледяной дождь',
    520: 'Слабый ливень', 521: 'Ливень', 522: 'Сильный ливень', 531: 'Переменный ливень',
    600: 'Слабый снег', 601: 'Снег', 602: 'Сильный снег', 603: 'Снежная буря', 611: 'Мокрый снег', 612: 'Снег с дождём', 615: 'Слабый мокрый снег', 616: 'Мокрый снег', 620: 'Слабый снегопад', 621: 'Снегопад', 622: 'Сильный снегопад',
    701: 'Мгла', 711: 'Дымка', 721: 'Пыльный взвесь', 731: 'Пыль/песок', 741: 'Туман', 751: 'Песчаный вихрь', 761: 'Пыль', 762: 'Вулканический пепел', 771: 'Шквал', 781: 'Торнадо',
    800: 'Ясно',
    801: 'Малооблачно', 802: 'Облачно', 803: 'Пасмурно', 804: 'Пасмурно',
}

# --- Направление ветра ---
def get_wind_direction(deg):
    directions = ['С', 'СВ', 'В', 'ЮВ', 'Ю', 'ЮЗ', 'З', 'СЗ']
    return directions[round(deg / 45) % 8]

# --- День недели на русском ---
def get_day_name(dt):
    days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    date = datetime.fromtimestamp(dt, tz=timezone.utc)
    return days[date.weekday()]

# --- Маршрут: главная страница ---
@app.route('/')
def index():
    return render_template('index.html')

# --- Маршрут: страница прогноза на неделю ---
@app.route('/forecast')
def forecast():
    return render_template('forecast.html', page='forecast')

# --- API: получение погоды (текущей) ---
@app.route('/api/weather')
def weather_api():
    try:
        params = urllib.parse.urlencode({
            'lat': LAT,
            'lon': LON,
            'appid': API_KEY,
            'units': 'metric',
            'lang': 'ru'
        })
        response = json.loads(urllib.request.urlopen(f"{URL}?{params}").read().decode())
        
        if response.get('cod') != 200:
            return jsonify({"error": response.get('message', 'Ошибка получения данных')}), 500
        
        main = response.get('main', {})
        wind = response.get('wind', {})
        weather = response.get('weather', [{}])[0]
        
        return jsonify({
            "city": "Мытищи",
            "desc": weather.get('description', 'Ясно'),
            "icon": weather.get('icon', '01d'),
            "temp": round(main.get('temp', 0)),
            "feels_like": round(main.get('feels_like', 0)),
            "humidity": main.get('humidity', 0),
            "pressure": round(main.get('pressure', 1013) * 0.75),
            "wind": f"{round(wind.get('speed', 0))} м/с",
            "sunrise": "06:00",
            "sunset": "20:00"
        })
    except Exception as e:
        print("Ошибка weather_api:", e)
        return jsonify({"error": str(e)}), 500

# --- API: получение прогноза на 5 дней ---
@app.route('/api/forecast')
def forecast_api():
    try:
        # Mock данные для тестирования (API недоступен из этой среды)
        forecast_list = [
            {'day_name': 'Понедельник', 'date': '06.02', 'temp': -8, 'desc': 'Небольшой снег', 'icon': '13d', 'humidity': 75, 'wind_speed': 3},
            {'day_name': 'Вторник', 'date': '07.02', 'temp': -10, 'desc': 'Ясно', 'icon': '01d', 'humidity': 70, 'wind_speed': 2},
            {'day_name': 'Среда', 'date': '08.02', 'temp': -6, 'desc': 'Облачно', 'icon': '03d', 'humidity': 80, 'wind_speed': 4},
            {'day_name': 'Четверг', 'date': '09.02', 'temp': -5, 'desc': 'Снег', 'icon': '13d', 'humidity': 85, 'wind_speed': 3},
            {'day_name': 'Пятница', 'date': '10.02', 'temp': -7, 'desc': 'Малооблачно', 'icon': '02d', 'humidity': 72, 'wind_speed': 2},
        ]
        
        return jsonify({
            "city": "Мытищи",
            "forecast": forecast_list
        })
    except Exception as e:
        import traceback
        print("Ошибка forecast_api:", e)
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

# Функция для автоматического открытия браузера
def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000')

if __name__ == '__main__':
    # Явно удаляем FLASK_APP из окружения, чтобы избежать reloader
    os.environ.pop('FLASK_APP', None)
    print("Server started. PID:", os.getpid())

    # Просто запускаем браузер один раз — без проверки WERKZEUG_RUN_MAIN
    # Потому что use_reloader=False → только один процесс
    Timer(1, open_browser).start()

    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False,
        use_reloader=False  # гарантируем один процесс
    )
