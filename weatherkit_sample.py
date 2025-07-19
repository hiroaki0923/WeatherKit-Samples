"""
weatherkit_sample.py - Sample code to call Apple WeatherKit REST API using Python

Prerequisites:
- Install dependencies using uv: uv sync
- Copy .env.example to .env and fill in your Apple Developer credentials
- Obtain your WeatherKit key file (AuthKey_XXXXXXXXXX.p8) from your Apple Developer account

Note: PyJWT requires the cryptography package for ES256 algorithm support
"""

import os
import time
from datetime import datetime
from zoneinfo import ZoneInfo
import jwt  # PyJWT
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ===== Configuration from environment =====
TEAM_ID = os.getenv("TEAM_ID")
KEY_ID = os.getenv("KEY_ID")
SERVICE_ID = os.getenv("SERVICE_ID")
KEY_FILE = os.getenv("KEY_FILE", f"AuthKey_{KEY_ID}.p8" if KEY_ID else "")

# Validate configuration
if not all([TEAM_ID, KEY_ID, SERVICE_ID, KEY_FILE]):
    raise ValueError(
        "Missing required environment variables. "
        "Please copy .env.example to .env and fill in your credentials."
    )

# ===== Generate JWT =====
def generate_weatherkit_jwt():
    # Read private key
    with open(KEY_FILE, "r") as f:
        private_key = f.read()

    # JWT headers and claims
    headers = {"alg": "ES256", "kid": KEY_ID}
    now = int(time.time())
    payload = {
        "iss": TEAM_ID,
        "iat": now,
        "exp": now + 3600,        # 1 hour validity
        "aud": "weatherkit",
        "sub": SERVICE_ID
    }

    token = jwt.encode(payload, private_key, algorithm="ES256", headers=headers)
    return token

# ===== Fetch Weather Data =====
def fetch_weather(latitude, longitude):
    token = generate_weatherkit_jwt()
    # URL形式を修正（語種の指定が必要）
    url = f"https://weatherkit.apple.com/api/v1/weather/ja/{latitude}/{longitude}"
    params = {
        "dataSets": "currentWeather,forecastHourly",  # Choose datasets
        "language": "ja",      # e.g. "en", "ja"
        "timezone": "Asia/Tokyo",
        "units": "metric"
    }
    headers = {"Authorization": f"Bearer {token}"}

    resp = requests.get(url, headers=headers, params=params)
    resp.raise_for_status()
    return resp.json()

# ===== Main Execution =====
if __name__ == "__main__":
    # Example: Coordinates for Tokyo Station
    lat, lon = 35.681236, 139.767125
    weather_data = fetch_weather(lat, lon)

    # Print current weather
    current = weather_data["currentWeather"]
    print("=== 現在の天気（東京駅） ===")
    print(f"気温: {current['temperature']:.1f}°C")
    print(f"体感温度: {current['temperatureApparent']:.1f}°C") 
    print(f"天候: {current['conditionCode']}")
    print(f"雲量: {current['cloudCover'] * 100:.0f}%")
    print(f"湿度: {current['humidity'] * 100:.0f}%")
    print(f"風速: {current['windSpeed']:.1f} m/s")

    # Print next 12 hours forecast
    print("\n=== 今後12時間の予報（日本時間） ===")
    if "forecastHourly" in weather_data and "hours" in weather_data["forecastHourly"]:
        # 日本時間のタイムゾーンを指定
        tokyo_tz = ZoneInfo("Asia/Tokyo")
        
        for hour in weather_data["forecastHourly"]["hours"][:12]:
            # キー名を確認しながら安全にアクセス
            forecast_time_str = hour.get("forecastStart", "N/A")
            temp = hour.get("temperature", "N/A")
            condition = hour.get("conditionCode", "N/A")
            # Cloud cover is returned as a ratio (0.0 - 1.0), convert to percentage
            cloud_cover = hour.get("cloudCover", 0)
            cloud_percent = cloud_cover * 100 if isinstance(cloud_cover, (int, float)) else 0
            
            # UTC時刻を日本時間に変換
            if forecast_time_str != "N/A":
                # ISO形式の文字列をdatetimeオブジェクトに変換（UTC）
                utc_time = datetime.fromisoformat(forecast_time_str.replace('Z', '+00:00'))
                # 日本時間に変換
                tokyo_time = utc_time.astimezone(tokyo_tz)
                # 見やすい形式でフォーマット
                time_str = tokyo_time.strftime("%m/%d %H:%M")
            else:
                time_str = "N/A"
            
            print(f"{time_str}: {temp}°C, {condition}, 雲量: {cloud_percent:.0f}%")
    else:
        print("時間ごとの予報データが利用できません。")
