# WeatherKit-Samples

Apple WeatherKit REST APIをPythonから利用するサンプルコード / Sample code for using Apple WeatherKit REST API with Python

## 概要 / Overview

このプロジェクトは、Apple WeatherKit REST APIをPythonから呼び出す方法を示すサンプルコードです。JWT認証を使用して、現在の天気情報と時間ごとの予報を取得します。

This project demonstrates how to call Apple WeatherKit REST API from Python. It uses JWT authentication to fetch current weather and hourly forecast data.

## 必要条件 / Prerequisites

- Python 3.8以上 / Python 3.8 or higher
- [uv](https://github.com/astral-sh/uv) (Pythonパッケージマネージャー / Python package manager)
- Apple Developer アカウント / Apple Developer account
- WeatherKit サービスが有効化されたApp ID / App ID with WeatherKit service enabled

### 依存パッケージ / Dependencies

- `PyJWT`: JWT認証用 / For JWT authentication
- `cryptography`: ES256アルゴリズムサポート用 / For ES256 algorithm support
- `requests`: HTTPリクエスト用 / For HTTP requests
- `python-dotenv`: 環境変数管理用 / For environment variable management

## セットアップ / Setup

### 1. uvのインストール / Install uv

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. プロジェクトのクローン / Clone the project

```bash
git clone https://github.com/yourusername/WeatherKit-Samples.git
cd WeatherKit-Samples
```

### 3. 依存関係のインストール / Install dependencies

```bash
uv sync
```

### 4. Apple Developer設定 / Apple Developer Configuration

#### プライベートキーの作成 / Create a Private Key

1. [Apple Developer](https://developer.apple.com/)にサインイン / Sign in to [Apple Developer](https://developer.apple.com/)
2. Certificates, Identifiers & Profilesに移動 / Navigate to Certificates, Identifiers & Profiles
3. **Keys**メニューを選択 / Select the **Keys** menu
4. **+** ボタンをクリックして新しいキーを作成 / Click **+** to create a new key
5. キーに名前を付け、**WeatherKit**を有効化 / Name your key and enable **WeatherKit**
6. **Continue**、**Register**の順にクリック / Click **Continue**, then **Register**
7. .p8形式のプライベートキーファイルをダウンロード（一度だけダウンロード可能） / Download the private key file in .p8 format (can only be downloaded once)
8. Key IDを記録 / Record your Key ID

#### Service IDの作成 / Create a Service ID

1. **Identifiers**メニューを選択 / Select the **Identifiers** menu
2. **+** ボタンをクリック / Click **+** to add
3. **Services IDs**を選択して**Continue** / Select **Services IDs** and click **Continue**
4. 説明とIDを設定（例: com.example.weatherkit-client） / Set a description and identifier (e.g., com.example.weatherkit-client)
5. **Continue**、**Register**の順にクリックして登録 / Click **Continue**, then **Register** to register the identifier

#### 必要な情報の確認 / Record Required Information

- **Team ID**: アカウント名の下に表示 / Displayed under your account name
- **Key ID**: 作成したキーのID / ID of the key you created
- **Service ID**: 作成したService IDの識別子 / Identifier of the Service ID you created

### 5. 環境変数の設定 / Configure environment variables

```bash
cp .env.example .env
```

`.env`ファイルを編集して、以下の値を設定 / Edit the `.env` file and set the following values:
- `TEAM_ID`: Apple Developer Team ID (例 / e.g.: ABCDE12345)
- `KEY_ID`: WeatherKit Key ID (例 / e.g.: ABCD1234EF)
- `SERVICE_ID`: Service ID (例 / e.g.: com.example.yourapp)
- `KEY_FILE`: .p8キーファイルのパス / Path to .p8 key file (例 / e.g.: AuthKey_ABCD1234EF.p8)

## 使い方 / Usage

### 基本的な使用方法 / Basic Usage

```bash
# デフォルト（東京駅）/ Default (Tokyo Station)
uv run python weatherkit_sample.py

# 任意の地点を指定 / Specify custom location
uv run python weatherkit_sample.py [緯度] [経度]
```

### 使用例 / Examples

```bash
# 東京駅の天気 / Weather for Tokyo Station (default)
uv run python weatherkit_sample.py

# サンフランシスコの天気 / Weather for San Francisco
uv run python weatherkit_sample.py 37.7749 -122.4194

# パリの天気 / Weather for Paris
uv run python weatherkit_sample.py 48.8566 2.3522

# シドニーの天気 / Weather for Sydney
uv run python weatherkit_sample.py -33.8688 151.2093
```

### 座標の取得方法 / How to Get Coordinates

Google Mapsで場所を右クリックし、座標をコピーできます。座標は「緯度, 経度」の順番で表示されます。

You can right-click on any location in Google Maps and copy the coordinates. Coordinates are displayed in "latitude, longitude" format.

## 出力例 / Example Output

```
=== データセット利用可能性の確認 ===
対象地点: (35.681236, 139.767125)
利用可能なデータセット: ['currentWeather', 'forecastDaily', 'forecastHourly', 'forecastNextHour']

取得するデータセット: currentWeather,forecastDaily,forecastHourly,forecastNextHour

=== 現在の天気 ===
気温: 26.7°C
体感温度: 26.6°C
天候: Cloudy
雲量: 89%
湿度: 83%
風速: 18.3 m/s

=== 今後12時間の予報（日本時間） ===
07/18 22:00: 26.1°C, MostlyCloudy, 雲量: 81%
07/18 23:00: 25.8°C, MostlyCloudy, 雲量: 82%
07/19 00:00: 25.5°C, MostlyCloudy, 雲量: 82%
...

=== 今後7日間の予報 ===
07/19 (Sat): 32.4°C / 25.0°C, MostlyCloudy
07/20 (Sun): 32.8°C / 24.9°C, PartlyCloudy
07/21 (Mon): 33.1°C / 24.9°C, PartlyCloudy
...

=== 次1時間の詳細予報 ===
データポイント数: 83分間
最初のデータ: 降水確率 0%, 降水強度 0.0mm/h
```

## ライセンス / License

Apache License 2.0 - 詳細は[LICENSE](LICENSE)ファイルを参照してください / See the [LICENSE](LICENSE) file for details.

## 注意事項 / Notes

- WeatherKit APIの利用には使用制限があります。詳細は[Apple Developer Documentation](https://developer.apple.com/documentation/weatherkit)を確認してください / WeatherKit API has usage limits. See [Apple Developer Documentation](https://developer.apple.com/documentation/weatherkit) for details.
- プライベートキーファイル(.p8)は絶対にGitリポジトリにコミットしないでください / Never commit private key files (.p8) to your Git repository.
- 本番環境では、認証情報を安全に管理してください / In production, manage your credentials securely.