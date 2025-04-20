# HNSW (Hierarchical Navigable Small World)を用いた類似画像検索

## 概要

このアプリは、写真をアップロードすることで、その写真と似ている画像をサンプル画像の中から検索します。

## 主な機能

1. サンプル画像の収集と前処理。
2. 特徴量の抽出と類似画像検索。
3. アップロードした画像に基づく画像類似検索結果の提供。

## 使用方法

### 1. 仮想環境のセットアップ

以下のコマンドを実行して仮想環境を作成し、必要なライブラリをインストールします。

```bash
python -m venv venv
source venv/bin/activate  # Windowsの場合は venv\Scripts\activate
pip install -r requirements.txt
```

### 2. テスト用にサンプル画像をダウンロードする `download_tiles.py`

8 行目の query にダウンロードしたい画像の検索文字列を代入します。

`query = "ceramic tile glaze glossy matte color texture"`

```bash
python download_tiles.py
```

実行後、収集された画像は `tiles_raw/` ディレクトリに保存されます。

**注意**: このスクリプトを使用しない場合、`tiles_raw/` ディレクトリに手動で画像を配置してください。

### 3. サンプル画像の前処理 `preprocess_tiles.py`

収集した画像をリサイズ（224x224）し、センタークロップを行います。

```bash
python preprocess_tiles.py
```

実行後、前処理済みの画像は `tiles/` ディレクトリに保存されます。

### 4. インデックス作成 `save_index.py`

前処理済みの画像から特徴量を抽出し、検索用のインデックスを作成します。

```bash
python save_index.py
```

実行後、インデックスデータは `index/` ディレクトリに保存されます。

### 5. サーバーの起動

以下のコマンドで FastAPI サーバーを起動します。

```bash
uvicorn main:app --reload
```

サーバーは `http://127.0.0.1:8000` で動作します。

### 6. 画像のアップロード

`post_to_search.py` を使用して画像をアップロードします。

14 行目`file_path = "source/test_tile_1.jpg"`を検索したい画像ファイルのパスに変更します。

```bash
python post_to_search.py
```

類似度の近いものから５つ出力される。

```bash
Response: {'results': [{'image_path': 'tiles/tile_092.jpg', 'distance': 0.16652733087539673}, {'image_path': 'tiles/tile_083.jpg', 'distance': 0.17888706922531128}, {'image_path': 'tiles/tile_029.jpg', 'distance': 0.18781429529190063}, {'image_path': 'tiles/tile_021.jpg', 'distance': 0.19300192594528198}, {'image_path': 'tiles/tile_069.jpg', 'distance': 0.19893264770507812}]}
```

---

## ディレクトリ構成

```
.
├── main.py               # FastAPIエントリーポイント
├── search_engine.py      # 類似検索エンジン
├── preprocess_tiles.py   # 画像前処理スクリプト
├── download_tiles.py     # サンプル画像収集スクリプト
├── save_index.py         # インデックス作成スクリプト
├── post_to_search.py     # 画像アップロードスクリプト
├── tiles/                # 前処理済みサンプル画像
├── tiles_raw/            # 生のサンプル画像
├── index/                # 検索インデックス
└── requirements.txt      # 必要なライブラリ
```

## 注意事項

- `tiles/`, `tiles_raw/`, `index/` ディレクトリは `.gitignore` に追加されており、Git 管理から除外されています。
- 入力画像の品質が結果に影響するため、できるだけ高解像度の画像を使用してください。

## ライセンス

このプロジェクトは MIT ライセンスの下で提供されています。
