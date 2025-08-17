# ヤドン デスクトップペット / Yadon Desktop Pet

ヤドン（Slowpoke）のかわいいデスクトップペットアプリケーションです。
A cute Slowpoke desktop pet application.

## 特徴 / Features

- 16x16ピクセルアートのヤドン
- ゆっくりとした動き（ヤドンらしい！）
- 画面の端で休憩
- ダブルクリックでメッセージ表示（すべて「やぁん」で終わります）
- ドラッグで移動可能
- Windows、macOS、Linux対応

## 必要要件 / Requirements

- Python 3.9+
- PyQt6 6.5.0
- Pillow 9.0+

## インストール / Installation

### Windows

1. Python 3.9以上をインストール
2. コマンドプロンプトまたはPowerShellを開く
3. 以下のコマンドを実行：

```cmd
cd yadon-desktop-pet
pip install -r requirements.txt
python desktop_pet.py
```

### macOS

1. ターミナルを開く
2. 以下のコマンドを実行：

```bash
cd yadon-desktop-pet
pip3 install -r requirements.txt
python3 desktop_pet.py
```

### Linux

1. ターミナルを開く
2. 以下のコマンドを実行：

```bash
cd yadon-desktop-pet
pip3 install -r requirements.txt
python3 desktop_pet.py
```

## 使い方 / Usage

- **ドラッグ**: 左クリックしてドラッグでヤドンを移動
- **ダブルクリック**: メッセージを表示
- **自動移動**: ヤドンは自動的にゆっくり動き回ります
- **休憩**: 画面の端（文字が少ない場所）で長めに休憩します

## トラブルシューティング / Troubleshooting

### Windows
- ヤドンが表示されない場合は、ウイルス対策ソフトの例外リストに追加してください
- タスクバーにアイコンが表示されない仕様です（Tool flagによる）

### macOS
- PyQt6のバージョンエラーが出た場合は、6.5.0を指定してインストールしてください
- 他のアプリをクリックしてもヤドンは消えません

### Linux
- ウィンドウマネージャーによって挙動が異なる場合があります
- X11環境で最適に動作します

## ライセンス / License

Personal use only

## 作者 / Author

ヤドンコーディング with Claude Code 🦥やぁん