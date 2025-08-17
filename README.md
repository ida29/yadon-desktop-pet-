# ヤドンデスクトップペット 🦦

Claude Codeのプロセスを監視し、フック機能と連携して吹き出しを表示するヤドン（Slowpoke）のデスクトップペットアプリケーションです。

## 機能

- **ピクセルアートのヤドン**: 16x16ピクセルアートで顔がアニメーション
- **Claude Code連携**: Claude Codeのプロセスを監視してPIDを表示
- **フック対応**: Claude Codeのフックに反応して吹き出しを表示
- **自動起動**: システム起動時に自動的に起動可能（macOS）
- **複数ヤドン対応**: 複数のClaude Codeプロセスに対して複数のヤドンを生成
- **スマート吹き出し**: ポケモンスタイルのテキストボックスが画面端で自動調整

## インストール

### 前提条件

```bash
# Python 3とPyQt6をインストール
pip install PyQt6
```

### クイックインストール（macOS）

```bash
# リポジトリをクローン
git clone https://github.com/ida29/yadon-desktop-pet-.git
cd yadon-desktop-pet-

# 自動起動用のインストールスクリプトを実行
./install.sh
```

### 手動実行

```bash
python3 yadon_pet.py
```

## Claude Codeフック統合

### Claude Codeでフックを設定

`~/.claude/settings.json`に以下を追加：

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/yadon-desktop-pet-/hook_notify.sh"
          }
        ]
      }
    ],
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/yadon-desktop-pet-/hook_stop.sh"
          }
        ]
      }
    ]
  }
}
```

**注意**: `/path/to/`をインストールディレクトリの実際のパスに置き換えてください。

### 利用可能なフック

- **Stopフック** (`hook_stop.sh`): Claude Codeが停止時に「ひとやすみするやぁん」を表示
- **Notificationフック** (`hook_notify.sh`): 通知時に「びびっときたやぁん」を表示

### カスタムフックメッセージ

フックファイルに書き込むことでヤドンにカスタムメッセージを送信できます：

```bash
# {PID}をClaude CodeのプロセスID（ヤドンの下に表示）に置き換え
echo "メッセージ" > /tmp/yadon_hook_{PID}.txt

# または汎用フックファイルを使用（最初のヤドンが応答）
echo "メッセージ" > /tmp/yadon_hook.txt
```

## 設定

### メイン設定（`config.py`）

- **ウィンドウサイズ**: 64x84ピクセル（PID表示込み）
- **PID表示**: Claude CodeのプロセスIDを表示（フォントサイズ12、太字）
- **アニメーション間隔**: 500ミリ秒ごとに顔アニメーション
- **ランダムアクション**: 45〜90秒ごと
- **移動**: ゆっくりした最小限の動き（移動に15秒、ヤドンらしい）
- **吹き出し表示時間**: 5秒

### 吹き出し機能

- ポケモンスタイルのダブルボーダーテキストボックス
- 長いメッセージの自動改行
- スマートポジショニング：
  - デフォルト：ヤドンの上
  - 上に空間がない場合：ヤドンの下
  - 縦方向に空間がない場合：ヤドンの横（位置に応じて左右）
- フックメッセージ（ライトシアン）と通常メッセージ（白）で色分け
- 移動中もスムーズに追従

## ファイル構造

```
yadon-desktop-pet-/
├── yadon_pet.py           # メインアプリケーション
├── config.py               # 設定定数
├── pixel_data.py           # ヤドンのスプライトデータ
├── speech_bubble.py        # 吹き出しウィジェット
├── process_monitor.py      # Claude Codeプロセス監視
├── hook_handler.py         # フックメッセージ処理
├── hook_notify.sh          # 通知フックスクリプト
├── hook_stop.sh           # 停止フックスクリプト
├── com.yadon.pet.plist    # macOS LaunchAgent設定
├── install.sh             # インストールスクリプト
└── requirements.txt       # Python依存関係
```

## 自動起動管理（macOS）

### 自動起動を有効化
```bash
./install.sh
```

### 自動起動を無効化
```bash
launchctl unload ~/Library/LaunchAgents/com.yadon.pet.plist
```

### 完全削除
```bash
launchctl unload ~/Library/LaunchAgents/com.yadon.pet.plist
rm ~/Library/LaunchAgents/com.yadon.pet.plist
```

## トラブルシューティング

### ヤドンが表示されない
- プロセスが実行中か確認：`ps aux | grep yadon_pet`
- ログを確認：`tail -f /tmp/yadon-pet.log`
- エラーログを確認：`tail -f /tmp/yadon-pet-error.log`

### フックが動作しない
- Claude Code PIDを確認：ヤドンの下に表示される番号を確認
- フックデバッグログを確認：`tail -f /tmp/hook_debug.log`
- フックスクリプトが実行可能か確認：`chmod +x hook_*.sh`
- `~/.claude/settings.json`のパスがインストール場所と一致しているか確認

### 吹き出しの位置がおかしい
- 吹き出しは画面端に基づいて自動的に位置を調整
- ヤドンが上端にいる場合、吹き出しは下に表示
- 下端にいる場合、吹き出しは上に表示
- 縦方向に空間がない場合、吹き出しは横に表示

### 複数のClaude Codeインスタンス
- 各Claude Codeプロセスに対して個別のヤドンが生成
- 各ヤドンは関連するClaude CodeのPIDを表示
- フックメッセージはPIDに基づいて正しいヤドンにルーティング

## デバッグログ

- **メインログ**: `/tmp/yadon-pet.log`
- **エラーログ**: `/tmp/yadon-pet-error.log`
- **デバッグログ**: `/tmp/yadon_debug.log`
- **フックデバッグ**: `/tmp/hook_debug.log`

## ライセンス

MIT License

## クレジット

Claude Codeで作成 - Claude Codeセッションのためのピクセルアートヤドンコンパニオン！

やぁん 🦥