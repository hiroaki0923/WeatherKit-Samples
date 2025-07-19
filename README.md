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

```bash
uv run python weatherkit_sample.py
```

デフォルトでは東京駅の天気情報を取得します。座標を変更したい場合は、`weatherkit_sample.py`の以下の行を編集してください / By default, it fetches weather for Tokyo Station. To change the location, edit the following line in `weatherkit_sample.py`:

```python
lat, lon = 35.681236, 139.767125  # 東京駅 / Tokyo Station
```

## 出力例 / Example Output

```
=== 現在の天気（東京駅） ===
気温: 28.2°C
体感温度: 28.0°C
天候: MostlyCloudy
雲量: 83%
湿度: 76%
風速: 18.9 m/s

=== 今後12時間の予報（日本時間） ===
07/19 19:00: 28.4°C, MostlyCloudy, 雲量: 85%
07/19 20:00: 27.6°C, MostlyCloudy, 雲量: 78%
07/19 21:00: 26.9°C, MostlyCloudy, 雲量: 82%
...
```

## ライセンス / License

Apache License 2.0 - 詳細は[LICENSE](LICENSE)ファイルを参照してください / See the [LICENSE](LICENSE) file for details.

## 注意事項 / Notes

- WeatherKit APIの利用には使用制限があります。詳細は[Apple Developer Documentation](https://developer.apple.com/documentation/weatherkit)を確認してください / WeatherKit API has usage limits. See [Apple Developer Documentation](https://developer.apple.com/documentation/weatherkit) for details.
- プライベートキーファイル(.p8)は絶対にGitリポジトリにコミットしないでください / Never commit private key files (.p8) to your Git repository.
- 本番環境では、認証情報を安全に管理してください / In production, manage your credentials securely.