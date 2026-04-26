from flask import Flask, render_template, jsonify
import requests
import urllib.parse
import json
import time
from datetime import datetime, timezone, timedelta
import os
import subprocess
from dotenv import load_dotenv
from cachetools import TTLCache

def get_version():
    """Получает версию приложения на основе git коммита и timestamp.
    
    Returns:
        str: Строка вида 'commit-timestamp' или текущая дата и время в формате YYYYMMDDHHMMSS
             если git недоступен.
    """
    try:
        commit = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode().strip()
        # Также берем timestamp коммита
        timestamp = subprocess.check_output(['git', 'log', '-1', '--format=%ct', 'HEAD']).decode().strip()
        return f"{commit}-{timestamp}"
    except:
        return datetime.now().strftime('%Y%m%d%H%M%S')

# Загружаем переменные окружения из .env
load_dotenv()

app = Flask(__name__)

# Версия для cache busting
VERSION = get_version()

# --- Настройки из переменных окружения ---
# OpenWeatherMap API endpoints
# Используем отдельные URL для текущей погоды и прогноза
URL = "https://api.openweathermap.org/data/2.5/weather"
URL_FORECAST = "https://api.openweathermap.org/data/2.5/forecast"
# API ключ берется из переменных окружения с fallback на placeholder
# В продакшене ОБЯЗАТЕЛЬНО установить реальный API ключ в .env файле
API_KEY = os.environ.get('API_KEY', 'your_api_key_here')

# Валидация обязательных переменных окружения
# LAT и LON критически важны для работы приложения - без них невозможно получить погоду
LAT = os.environ.get('LAT')
LON = os.environ.get('LON')
if not LAT or not LON:
    raise ValueError("Переменные окружения LAT и LON должны быть заданы в .env файле")

# Преобразуем строки в числа с плавающей точкой для использования в API запросах
LAT = float(LAT)
LON = float(LON)

# Таймаут для запросов к API (в секундах)
# Значение 10 секунд выбрано как компромисс между ожиданием ответа и пользовательским опытом
# При превышении таймаута используется кешированные данные если они доступны
API_TIMEOUT = 10

# Кеш для хранения последних данных с автоматическим временем жизни
# Используется для уменьшения количества запросов к OpenWeatherMap API
# TTLCache автоматически удаляет устаревшие записи и потокобезопасен
CACHE_TTL = 300  # Время жизни кеша в секундах (5 минут)
weather_cache = TTLCache(maxsize=100, ttl=CACHE_TTL)
forecast_cache = TTLCache(maxsize=100, ttl=CACHE_TTL)

# Часовой пояс UTC+3 (Москва)
TZ_OFFSET = timezone(timedelta(hours=3))

# --- Коды погоды OpenWeatherMap -> иконки ---
# Маппинг кодов погоды OpenWeatherMap на имена файлов иконок
# Коды сгруппированы по типам погоды:
# 2xx: Гроза
# 3xx: Морось
# 5xx: Дождь
# 6xx: Снег
# 7xx: Атмосферные явления (туман, пыль и т.д.)
# 800: Ясно
# 80x: Облачность (от малооблачно до пасмурно)
OWM_TO_ICON = {
    # Гроза
    200: '11d', 201: '11d', 202: '11d', 210: '11d', 211: '11d', 212: '11d', 221: '11d', 230: '11d', 231: '11d', 232: '11d',
    # Морось
    300: '09d', 301: '09d', 302: '09d', 310: '09d', 311: '09d', 312: '09d', 313: '09d', 314: '09d', 321: '09d',
    # Дождь
    500: '10d', 501: '10d', 502: '10d', 503: '10d', 504: '10d', 511: '10d', 520: '09d', 521: '09d', 522: '09d', 531: '09d',
    # Снег
    600: '13d', 601: '13d', 602: '13d', 611: '13d', 612: '13d', 613: '13d', 615: '13d', 616: '13d', 620: '13d', 621: '13d', 622: '13d',
    # Атмосферные явления
    701: '50d', 711: '50d', 721: '50d', 731: '50d', 741: '50d', 751: '50d', 761: '50d', 762: '50d', 771: '50d', 781: '50d',
    # Ясно
    800: '01d',
    # Облачность
    801: '02d', 802: '03d', 803: '04d', 804: '04d',
}

# --- Коды погоды -> описание на русском ---
# Маппинг кодов погоды OpenWeatherMap на описания на русском языке
# Группировка по типам погоды аналогично OWM_TO_ICON
OWM_TO_DESC = {
    # Гроза
    200: 'Гроза с дождём', 201: 'Гроза с дождём', 202: 'Сильная гроза с дождём',
    210: 'Гроза', 211: 'Гроза', 212: 'Сильная гроза', 221: 'Сильная гроза', 230: 'Гроза с мокрым снегом', 231: 'Гроза с мокрым снегом', 232: 'Сильная гроза с мокрым снегом',
    # Морось
    300: 'Морось', 301: 'Морось', 302: 'Плотная морось', 310: 'Морось', 311: 'Морось', 312: 'Плотная морось', 313: 'Морось', 314: 'Плотная морось', 321: 'Плотная морось',
    # Дождь
    500: 'Слабый дождь', 501: 'Умеренный дождь', 502: 'Сильный дождь', 503: 'Очень сильный дождь', 504: 'Продолжительный дождь', 511: 'Ледяной дождь',
    520: 'Слабый ливень', 521: 'Ливень', 522: 'Сильный ливень', 531: 'Переменный ливень',
    # Снег
    600: 'Слабый снег', 601: 'Снег', 602: 'Сильный снег', 603: 'Снежная буря', 611: 'Мокрый снег', 612: 'Снег с дождём', 615: 'Слабый мокрый снег', 616: 'Мокрый снег', 620: 'Слабый снегопад', 621: 'Снегопад', 622: 'Сильный снегопад',
    # Атмосферные явления
    701: 'Мгла', 711: 'Дымка', 721: 'Пыльный взвесь', 731: 'Пыль/песок', 741: 'Туман', 751: 'Песчаный вихрь', 761: 'Пыль', 762: 'Вулканический пепел', 771: 'Шквал', 781: 'Торнадо',
    # Ясно
    800: 'Ясно',
    # Облачность
    801: 'Малооблачно', 802: 'Облачно', 803: 'Пасмурно', 804: 'Пасмурно',
}

# --- Направление ветра ---
def get_wind_direction(deg):
    """Преобразует направление ветра в градусах в текстовое представление.
    
    Args:
        deg (float): Направление ветра в градусах (0-360)
        
    Returns:
        str: Текстовое представление направления ветра (С, СВ, В, ЮВ, Ю, ЮЗ, З, СЗ)
    """
    directions = ['С', 'СВ', 'В', 'ЮВ', 'Ю', 'ЮЗ', 'З', 'СЗ']
    return directions[round(deg / 45) % 8]

# --- День недели на русском ---
def get_day_name(dt):
    """Преобразует timestamp в название дня недели на русском языке.
    
    Args:
        dt (int): Timestamp (секунды с эпохи)
        
    Returns:
        str: Название дня недели на русском языке
    """
    days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    date = datetime.fromtimestamp(dt, tz=timezone.utc)
    return days[date.weekday()]

# --- API: получение версии ---
@app.route('/api/version')
def version_api():
    return jsonify({"version": VERSION})

# --- Маршрут: главная страница ---
@app.route('/')
def index():
    return render_template('index.html', version=VERSION)

# --- Маршрут: страница прогноза на неделю ---
@app.route('/forecast')
def forecast():
    return render_template('forecast.html', page='forecast', version=VERSION)

# --- API: получение погоды (текущей) ---
@app.route('/api/weather')
def weather_api():
    """Получает текущую погоду для заданных координат с кешированием.
    
    Returns:
        Response: JSON ответ с данными о погоде или ошибкой
        
    Кеширование:
        Данные кешируются на CACHE_TTL секунд (по умолчанию 5 минут)
        чтобы уменьшить количество запросов к OpenWeatherMap API
        Используется потокобезопасный TTLCache из cachetools
    """
    # Пытаемся получить данные из кеша
    cached_data = weather_cache.get('data')
    if cached_data is not None:
        return jsonify(cached_data)
    
    try:
        params = urllib.parse.urlencode({
            'lat': LAT,
            'lon': LON,
            'appid': API_KEY,
            'units': 'metric',
            'lang': 'ru'
        })
        
        # Используем requests с таймаутом вместо urllib
        response = requests.get(f"{URL}?{params}", timeout=API_TIMEOUT)
        data = response.json()
        
        if data.get('cod') != 200:
            # Если есть закешированные данные, возвращаем их
            if weather_cache.get('data') is not None:
                return jsonify(weather_cache.get('data'))
            return jsonify({"error": data.get('message', 'Ошибка получения данных')}), 500
        
        main = data.get('main', {})
        wind = data.get('wind', {})
        weather = data.get('weather', [{}])[0]
        sys = data.get('sys', {})
        
        # Конвертируем timestamps рассвета и заката в локальное время (UTC+3)
        sunrise_ts = sys.get('sunrise', 0)
        sunset_ts = sys.get('sunset', 0)
        sunrise_time = datetime.fromtimestamp(sunrise_ts, tz=TZ_OFFSET).strftime('%H:%M')
        sunset_time = datetime.fromtimestamp(sunset_ts, tz=TZ_OFFSET).strftime('%H:%M')
        
        result = {
            "city": "Мытищи",
            "desc": weather.get('description', 'Ясно'),
            "icon": weather.get('icon', '01d'),
            "weather_id": weather.get('id', 800),
            "temp": round(main.get('temp', 0)),
            "feels_like": round(main.get('feels_like', 0)),
            "humidity": main.get('humidity', 0),
            "pressure": round(main.get('pressure', 1013) * 0.75),
            "wind": f"{round(wind.get('speed', 0))} м/с, {get_wind_direction(wind.get('deg', 0))}",
            "sunrise": sunrise_time,
            "sunset": sunset_time
        }
        
        # Обновляем кеш
        weather_cache['data'] = result
        
        return jsonify(result)
    except requests.exceptions.Timeout:
        print("Таймаут при запросе к API погоды")
        # Возвращаем закешированные данные если есть
        if weather_cache.get('data') is not None:
            return jsonify(weather_cache.get('data'))
        return jsonify({"error": "Превышен таймаут ожидания от сервера"}), 504
    except Exception as e:
        print("Ошибка weather_api:", e)
        # Возвращаем закешированные данные если есть
        if weather_cache.get('data') is not None:
            return jsonify(weather_cache.get('data'))
        return jsonify({"error": str(e)}), 500

# --- API: получение прогноза на 5 дней ---
@app.route('/api/forecast')
def forecast_api():
    """Получает прогноз погоды на 5 дней для заданных координат с кешированием.
    
    Returns:
        Response: JSON ответ с прогнозом погоды или ошибкой
        
    Кеширование:
        Данные кешируются на CACHE_TTL секунд (по умолчанию 5 минут)
        чтобы уменьшить количество запросов к OpenWeatherMap API
        Используется потокобезопасный TTLCache из cachetools
        
    Логика группировки:
        - OpenWeatherMap API возвращает прогноз с шагом 3 часа на 5 дней (40 записей)
        - Берется первая доступная запись прогноза на каждый день (обычно утренняя)
        - Исключается сегодняшний день из прогноза, чтобы показать только будущие дни
        - Возвращается максимум 5 дней прогноза (завтра и следующие 4 дня)
        - Для каждого дня берется температура, описание погоды, иконка, влажность и ветер
    """
    # Пытаемся получить данные из кеша
    cached_data = forecast_cache.get('data')
    if cached_data is not None:
        return jsonify(cached_data)
    
    try:
        params = urllib.parse.urlencode({
            'lat': LAT,
            'lon': LON,
            'appid': API_KEY,
            'units': 'metric',
            'lang': 'ru'
        })
        
        # Используем requests с таймаутом
        response = requests.get(f"{URL_FORECAST}?{params}", timeout=API_TIMEOUT)
        data = response.json()
        
        if data.get('cod') != '200':
            # Если есть закешированные данные, возвращаем их
            if forecast_cache.get('data') is not None:
                return jsonify(forecast_cache.get('data'))
            return jsonify({"error": data.get('message', 'Ошибка получения данных')}), 500
        
        # Получаем текущую дату в часовом поясе UTC+3
        # Это важно для правильного определения "сегодняшнего дня" в локальном времени
        today = datetime.now(TZ_OFFSET).date()
        tomorrow = today + timedelta(days=1)
        
        # Дни недели на русском языке для отображения в UI
        days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
        
        # Сортируем все записи прогноза по времени (от ранних к поздним)
        # Это гарантирует, что мы берем первую запись дня (обычно самую раннюю)
        forecast_items = sorted(data.get('list', []), key=lambda x: x.get('dt', 0))
        
        # Группируем данные по дням, беря первую доступную запись на каждый день
        # days_data будет содержать данные для каждого будущего дня
        days_data = {}
        for item in forecast_items:
            dt = item.get('dt', 0)
            # Преобразуем timestamp в локальное время (UTC+3 для Москвы)
            dt_local = datetime.fromtimestamp(dt, tz=TZ_OFFSET)
            day_date = dt_local.date()
            
            # Пропускаем сегодняшний день и все прошлые дни
            # Мы хотим показать только будущие дни в прогнозе
            if day_date <= today:
                continue
            
            # Формируем ключ дня в формате YYYY-MM-DD для группировки
            day_key = day_date.strftime('%Y-%m-%d')
            
            # Если мы еще не обрабатывали этот день, сохраняем данные о погоде
            if day_key not in days_data:
                weather = item.get('weather', [{}])[0]
                main = item.get('main', {})
                wind = item.get('wind', {})
                
                # Формируем объект с данными о погоде для этого дня
                days_data[day_key] = {
                    'day_name': days[dt_local.weekday()],  # День недели на русском
                    'date': dt_local.strftime('%d.%m'),    # Дата в формате DD.MM
                    'temp': round(main.get('temp', 0)),    # Температура в Цельсиях, округленная
                    'desc': OWM_TO_DESC.get(weather.get('id', 800), weather.get('description', 'Ясно')),
                    # Описание погоды на русском, с fallback на описание из API
                    'icon': weather.get('icon', '01d'),    # Иконка погоды (будет заменена на анимированную GIF)
                    'humidity': main.get('humidity', 0),   # Влажность в процентах
                    'wind_speed': f"{round(wind.get('speed', 0))} м/с, {get_wind_direction(wind.get('deg', 0))}"
                    # Ветер: скорость в м/с и направление (С, СВ, В и т.д.)
                }
        
        # Берем первые 5 дней из сгруппированных данных
        # Если данных меньше 5 дней (например, API вернул меньше записей), берем все доступные
        forecast_list = list(days_data.values())[:5]
        
        result = {
            "city": "Мытищи",  # Жестко заданный город для простоты демо-версии
            "forecast": forecast_list
        }
        
        # Обновляем кеш
        forecast_cache['data'] = result
        
        return jsonify(result)
    except requests.exceptions.Timeout:
        print("Таймаут при запросе к API прогноза")
        # Возвращаем закешированные данные если есть
        # Это повышает отказоустойчивость приложения при проблемах с сетью
        if forecast_cache.get('data') is not None:
            return jsonify(forecast_cache.get('data'))
        return jsonify({"error": "Превышен таймаут ожидания от сервера"}), 504
    except Exception as e:
        import traceback
        print("Ошибка forecast_api:", e)
        traceback.print_exc()
        # Возвращаем закешированные данные если есть
        # Это еще один механизм отказоустойчивости
        if forecast_cache.get('data') is not None:
            return jsonify(forecast_cache.get('data'))
        return jsonify({"error": str(e)}), 500

# Healthcheck endpoint для Docker
@app.route('/health')
def health():
    """Healthcheck endpoint для проверки работоспособности приложения.
    
    Returns:
        Response: JSON ответ со статусом 'ok' если приложение работает
        
    Используется Docker для проверки здоровья контейнера
    """
    return jsonify({"status": "ok"})
