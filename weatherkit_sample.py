"""
weatherkit_sample.py - Sample code to call Apple WeatherKit REST API using Python

Prerequisites:
- Install dependencies using uv: uv sync
- Copy .env.example to .env and fill in your Apple Developer credentials
- Obtain your WeatherKit key file (AuthKey_XXXXXXXXXX.p8) from your Apple Developer account

Note: PyJWT requires the cryptography package for ES256 algorithm support
"""

import os
import sys
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

# ===== Check Available Data Sets =====
def check_availability(latitude, longitude, country=None):
    token = generate_weatherkit_jwt()
    url = f"https://weatherkit.apple.com/api/v1/availability/{latitude}/{longitude}"
    headers = {"Authorization": f"Bearer {token}"}
    
    params = {}
    if country:
        params["country"] = country
    
    resp = requests.get(url, headers=headers, params=params)
    resp.raise_for_status()
    return resp.json()

# ===== Fetch Weather Data =====
def fetch_weather(latitude, longitude, datasets=None):
    token = generate_weatherkit_jwt()
    url = f"https://weatherkit.apple.com/api/v1/weather/ja/{latitude}/{longitude}"
    params = {
        "dataSets": datasets or "currentWeather,forecastHourly",  # Use provided datasets or default
        "language": "ja",      # e.g. "en", "ja"
        "timezone": "Asia/Tokyo",
        "units": "metric"
    }
    headers = {"Authorization": f"Bearer {token}"}

    resp = requests.get(url, headers=headers, params=params)
    resp.raise_for_status()
    return resp.json()

# ===== Parse Command Line Arguments =====
def parse_coordinates():
    """Parse latitude and longitude from command line arguments.
    
    Usage:
        python weatherkit_sample.py [latitude] [longitude]
        
    If no arguments provided, defaults to Tokyo Station coordinates.
    """
    # Default coordinates: Tokyo Station
    default_lat, default_lon = 35.681236, 139.767125
    
    if len(sys.argv) == 1:
        # No arguments provided, use default
        return default_lat, default_lon
    elif len(sys.argv) == 3:
        # Both latitude and longitude provided
        try:
            lat = float(sys.argv[1])
            lon = float(sys.argv[2])
            
            # Basic validation
            if not (-90 <= lat <= 90):
                print("エラー: 緯度は-90から90の範囲で入力してください")
                sys.exit(1)
            if not (-180 <= lon <= 180):
                print("エラー: 経度は-180から180の範囲で入力してください")
                sys.exit(1)
                
            return lat, lon
        except ValueError:
            print("エラー: 緯度と経度は数値で入力してください")
            print("使用方法: python weatherkit_sample.py [緯度] [経度]")
            print("例: python weatherkit_sample.py 35.681236 139.767125")
            sys.exit(1)
    else:
        print("エラー: 引数の数が正しくありません")
        print("使用方法: python weatherkit_sample.py [緯度] [経度]")
        print("例: python weatherkit_sample.py 35.681236 139.767125")
        print("引数なしの場合は東京駅の座標を使用します")
        sys.exit(1)

# ===== Main Execution =====
if __name__ == "__main__":
    # Parse coordinates from command line arguments
    lat, lon = parse_coordinates()
    
    # Check availability first
    print("=== データセット利用可能性の確認 ===")
    try:
        # Check availability with country parameter for Japan
        availability = check_availability(lat, lon, "JP")
        print(f"対象地点: ({lat:.6f}, {lon:.6f})")
        print(f"利用可能なデータセット: {availability}")
        
        # Use available datasets directly
        if availability:
            datasets_str = ",".join(availability)
            print(f"\n取得するデータセット: {datasets_str}")
            
            # Fetch weather data with available datasets
            weather_data = fetch_weather(lat, lon, datasets_str)
        else:
            print("利用可能なデータセットがありません。")
            exit(1)
            
    except Exception as e:
        print(f"Availability確認エラー: {e}")
        print("デフォルトのデータセットで試行します...")
        weather_data = fetch_weather(lat, lon)

    # Print current weather
    current = weather_data["currentWeather"]
    print("=== 現在の天気 ===")
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
        
        # 最初の時間データのフィールドを詳細分析
        if weather_data["forecastHourly"]["hours"]:
            first_hour = weather_data["forecastHourly"]["hours"][0]
            print("=== 利用可能なフィールド分析（最初の時間データ） ===")
            print("Required fields:")
            required_fields = [
                "cloudCover",           # 雲量（0-1）
                "conditionCode",        # 天気状態コード
                "forecastStart",        # 予報開始時刻
                "humidity",             # 湿度（0-1）
                "precipitationChance",  # 降水確率（0-1）
                "precipitationType",    # 降水タイプ
                "pressure",             # 気圧（ミリバール）
                "temperature",          # 気温（摂氏）
                "temperatureApparent",  # 体感温度（摂氏）
                "uvIndex",              # UV指数
                "visibility",           # 視程（メートル）
                "windSpeed"             # 風速（km/h）
            ]
            for field in required_fields:
                status = "✅" if field in first_hour else "❌"
                if status == "✅":
                    value = first_hour[field]
                    print(f"  {status} {field}: {value}")
                else:
                    print(f"  {status} {field}")
            
            print("\nOptional fields:")
            optional_fields = [
                # 基本的な気象データ
                "daylight",              # 昼/夜の判定
                "pressureTrend",         # 気圧変化の傾向
                "temperatureDewPoint",   # 露点温度（摂氏）
                # 風データ
                "windDirection",         # 風向（度）
                "windGust",              # 突風速度（km/h）
                # 降水・降雪データ
                "precipitationAmount",   # 降水量（mm）
                "snowfallIntensity"      # 降雪強度（mm/h）
            ]
            for field in optional_fields:
                status = "✅" if field in first_hour else "❌"
                if status == "✅":
                    value = first_hour[field]
                    print(f"  {status} {field}: {value}")
                else:
                    print(f"  {status} {field}")
            print("=" * 50)
        
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
                # ISO 8601形式のタイムスタンプを直接パース（Python 3.11+でZ対応）
                utc_time = datetime.fromisoformat(forecast_time_str)
                # 日本時間に変換
                tokyo_time = utc_time.astimezone(tokyo_tz)
                # 見やすい形式でフォーマット
                time_str = tokyo_time.strftime("%m/%d %H:%M")
            else:
                time_str = "N/A"
            
            print(f"{time_str}: {temp}°C, {condition}, 雲量: {cloud_percent:.0f}%")
    else:
        print("時間ごとの予報データが利用できません。")
    
    # Print daily forecast if available
    if "forecastDaily" in weather_data and "days" in weather_data["forecastDaily"]:
        print("\n=== 今後7日間の予報 ===")
        tokyo_tz = ZoneInfo("Asia/Tokyo")
        
        # 最初の日のデータでフィールドを詳細分析
        if weather_data["forecastDaily"]["days"]:
            first_day = weather_data["forecastDaily"]["days"][0]
            print("=== 利用可能なフィールド分析（最初の日データ） ===")
            print("Required fields:")
            required_fields = [
                "conditionCode",         # 天気状態コード
                "forecastEnd",           # 予報終了時刻
                "forecastStart",         # 予報開始時刻
                "maxUvIndex",            # 最大UV指数
                "moonPhase",             # 月相
                "precipitationAmount",   # 降水量（mm）
                "precipitationChance",   # 降水確率
                "precipitationType",     # 降水タイプ
                "snowfallAmount",        # 降雪量（mm）
                "temperatureMax",        # 最高気温（摂氏）
                "temperatureMin"         # 最低気温（摂氏）
            ]
            for field in required_fields:
                status = "✅" if field in first_day else "❌"
                if status == "✅":
                    value = first_day[field]
                    print(f"  {status} {field}: {value}")
                else:
                    print(f"  {status} {field}")
            
            print("\nOptional fields:")
            optional_fields = [
                # 昼夜の予報
                "daytimeForecast",       # 昼間（7AM-7PM）の予報
                "overnightForecast",     # 夜間（7PM-7AM）の予報
                # 月の出入り
                "moonrise",              # 月の出
                "moonset",               # 月の入り
                # 太陽関連時刻
                "solarMidnight",         # 太陽が最も低い時刻
                "solarNoon",             # 太陽が最も高い時刻
                "sunrise",               # 日の出
                "sunset",                # 日の入り
                # 薄明時刻
                "sunriseAstronomical",   # 天文薄明開始（太陽高度-18°）
                "sunriseCivil",          # 市民薄明開始（太陽高度-6°）
                "sunriseNautical",       # 航海薄明開始（太陽高度-12°）
                "sunsetAstronomical",    # 天文薄明終了（太陽高度-18°）
                "sunsetCivil",           # 市民薄明終了（太陽高度-6°）
                "sunsetNautical"         # 航海薄明終了（太陽高度-12°）
            ]
            for field in optional_fields:
                status = "✅" if field in first_day else "❌"
                if status == "✅":
                    value = first_day[field]
                    # ネストされたオブジェクトの場合は簡潔に表示
                    if isinstance(value, dict):
                        value = f"{{...}} (ネストされたオブジェクト)"
                    print(f"  {status} {field}: {value}")
                else:
                    print(f"  {status} {field}")
            print("=" * 50)
        
        for day in weather_data["forecastDaily"]["days"][:7]:
            forecast_date_str = day.get("forecastStart", "N/A")
            temp_max = day.get("temperatureMax", "N/A")
            temp_min = day.get("temperatureMin", "N/A")
            condition = day.get("conditionCode", "N/A")
            
            # UTC日付を日本時間に変換
            if forecast_date_str != "N/A":
                # ISO 8601形式のタイムスタンプを直接パース（Python 3.11+でZ対応）
                utc_date = datetime.fromisoformat(forecast_date_str)
                tokyo_date = utc_date.astimezone(tokyo_tz)
                date_str = tokyo_date.strftime("%m/%d (%a)")
            else:
                date_str = "N/A"
            
            print(f"{date_str}: {temp_max}°C / {temp_min}°C, {condition}")
    
    # Print next hour forecast if available
    if "forecastNextHour" in weather_data and "minutes" in weather_data["forecastNextHour"]:
        print(f"\n=== 次1時間の詳細予報 ===")
        minutes_data = weather_data["forecastNextHour"]["minutes"]
        print(f"データポイント数: {len(minutes_data)}分間")
        if minutes_data:
            first_minute = minutes_data[0]
            print(f"最初のデータ: 降水確率 {first_minute.get('precipitationChance', 0)*100:.0f}%, 降水強度 {first_minute.get('precipitationIntensity', 0):.1f}mm/h")
