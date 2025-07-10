# Universal Scaffold Tool

[![Go Version](https://img.shields.io/badge/Go-1.23+-blue.svg)](https://golang.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Universal Scaffold Tool は、様々な技術スタックに対応可能な汎用的なコード生成ツールです。Rails や Laravel のようなスキャフォールド機能を、あらゆるプロジェクトで利用できるようにすることを目的としています。

## 🚀 特徴

- **技術スタック非依存**: C#/.NET、Python、React、Go、Rust など様々な言語・フレームワークに対応
- **AI統合**: Claude Code、Cursor AI、MCP (Model Context Protocol) との深い統合
- **カテゴリ別組織化**: テンプレートを目的別にカテゴリ分けして管理
- **階層テンプレート**: 複数の`.scaffold`ディレクトリからの設定マージ機能
- **モダン開発環境**: mise + uv、Docker、FastAPI などの最新ツール対応
- **テンプレートベース**: プレーンテキストファイルを使用した柔軟なテンプレート管理
- **TOML設定**: シンプルで読みやすい設定ファイル形式
- **変数展開**: `{{variable}}` 形式での動的コンテンツ生成
- **ディレクトリ自動作成**: 必要なディレクトリ構造を自動で作成
- **上書き保護**: 既存ファイルの上書き確認機能

## 📦 インストール

### 🚀 バイナリダウンロード（推奨）

最新リリースから直接ダウンロードして即座に使用開始できます：

#### Linux
```bash
# x64 (最も一般的)
curl -L https://github.com/mitakeck/scaffold/releases/latest/download/scaffold-linux-amd64 -o scaffold
chmod +x scaffold
sudo mv scaffold /usr/local/bin/

# ARM64
curl -L https://github.com/mitakeck/scaffold/releases/latest/download/scaffold-linux-arm64 -o scaffold
chmod +x scaffold
sudo mv scaffold /usr/local/bin/
```

#### macOS
```bash
# Apple Silicon (M1/M2/M3) - 新しいMac推奨
curl -L https://github.com/mitakeck/scaffold/releases/latest/download/scaffold-darwin-arm64 -o scaffold
chmod +x scaffold
sudo mv scaffold /usr/local/bin/

# Intel - 古いMac
curl -L https://github.com/mitakeck/scaffold/releases/latest/download/scaffold-darwin-amd64 -o scaffold
chmod +x scaffold
sudo mv scaffold /usr/local/bin/
```

#### Windows
PowerShellを管理者として実行：
```powershell
# x64 (最も一般的)
Invoke-WebRequest -Uri "https://github.com/mitakeck/scaffold/releases/latest/download/scaffold-windows-amd64.exe" -OutFile "scaffold.exe"
Move-Item scaffold.exe C:\Windows\System32\scaffold.exe

# ARM64
Invoke-WebRequest -Uri "https://github.com/mitakeck/scaffold/releases/latest/download/scaffold-windows-arm64.exe" -OutFile "scaffold.exe"
Move-Item scaffold.exe C:\Windows\System32\scaffold.exe
```

### 🔧 ソースからビルド

開発者向け、またはカスタマイズが必要な場合：

#### 必要要件
- Go 1.23+
- [mise](https://mise.jdx.dev/) (推奨)

#### ビルド方法
```bash
# リポジトリをクローン
git clone https://github.com/mitakeck/scaffold.git
cd scaffold

# miseを使用してビルド
mise install
mise exec -- go build -o scaffold main.go

# または直接Goでビルド
go build -o scaffold main.go
```

### ✅ インストール確認

```bash
# コマンドが認識されることを確認
scaffold --help

# カテゴリ一覧表示
scaffold

# 簡単なテンプレート生成テスト
scaffold devtools makefile-advanced test-project
```

### 🚨 トラブルシューティング

#### Linuxで実行時にpermission deniedエラー
```bash
# 実行権限を付与
chmod +x scaffold
```

#### macOSで「開発元が未確認」エラー
```bash
# 一時的に実行を許可
sudo xattr -r -d com.apple.quarantine scaffold

# または、システム設定 > セキュリティとプライバシー で許可
```

#### コマンドが見つからない (command not found)
```bash
# PATHに追加されているか確認
echo $PATH | grep /usr/local/bin

# 手動でPATHに追加 (bashの場合)
echo 'export PATH="/usr/local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# 手動でPATHに追加 (zshの場合)
echo 'export PATH="/usr/local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

#### Windows PowerShell実行ポリシーエラー
```powershell
# 実行ポリシーを一時的に変更
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 🎁 その他のインストール方法

#### Homebrewでのインストール（計画中）
```bash
# 将来的にサポート予定
brew install mitakeck/tap/scaffold
```

#### パッケージマネージャーでのインストール（計画中）
```bash
# apt (Ubuntu/Debian) - 将来的にサポート予定
sudo apt install scaffold

# yum/dnf (RHEL/CentOS/Fedora) - 将来的にサポート予定  
sudo dnf install scaffold
```

## 🏗️ 使用方法

### 基本コマンド

```bash
# 利用可能なカテゴリ一覧
./scaffold

# カテゴリ内のテンプレート一覧
./scaffold <category> list

# テンプレートの詳細情報
./scaffold <category> info <template>

# ファイル生成
./scaffold <category> <template> [args...] [key=value...]
```

## 📂 テンプレートカテゴリ

### 🏛️ C#/.NET アーキテクチャ (`csharp`)

DDD（ドメイン駆動設計）とClean Architectureに基づいたC#テンプレート群

```bash
# ユースケース生成
./scaffold csharp usecase Application Users CreateUser author="開発者名"

# ドメインエンティティ生成
./scaffold csharp entity Domain Users User

# 値オブジェクト生成
./scaffold csharp valueobject Domain Users Email

# リポジトリ生成（インターフェース + 実装）
./scaffold csharp repository Domain Users User

# ドメイン例外クラス生成
./scaffold csharp exception Domain Users EUS_001_001 UserNameRequired

# Web APIコントローラー生成
./scaffold csharp webapi-controller Presentation Users User
```

### 🌐 Web開発 (`web`)

モダンなフロントエンド開発のためのテンプレート群

```bash
# Reactコンポーネント生成（TypeScript）
./scaffold web react-component UserProfile author="開発者名"

# Vite + React + TypeScript プロジェクト生成
./scaffold web vite-react-ts my-awesome-app
```

### 🛠️ 開発ツール (`devtools`)

開発効率化のためのツールテンプレート群

```bash
# 高機能Makefile生成（自動ドキュメント生成付き）
./scaffold devtools makefile-advanced my-project type=node

# GitHub Actions CI/CD ワークフロー生成
./scaffold devtools github-actions-ci node my-ci-workflow
```

### 🤖 AI開発支援 (`ai`)

Claude Code、Cursor AI、MCP統合を含むAI開発プロジェクトのテンプレート群

```bash
# Cursor AI用.cursorrules生成（技術スタック別）
./scaffold ai claude-cursorrules react author="開発者名"
./scaffold ai claude-cursorrules python author="開発者名"
./scaffold ai claude-cursorrules go author="開発者名"

# MCP (Model Context Protocol) サーバー生成
./scaffold ai claude-mcp-server file-manager typescript

# Claude Code カスタムコマンド生成
./scaffold ai claude-commands refactor "Code refactoring assistant"

# AI開発プロジェクト初期化
./scaffold ai claude-project-init my-ai-project

# Claude Code マルチエージェント通信システム
./scaffold ai claude-multiagent my-team-project
```

### 🐍 Python開発 (`python`)

モダンなPython開発のためのテンプレート群（mise + uv対応）

```bash
# FastAPI REST APIサービス生成
./scaffold python fastapi-service user-api user_api author="開発者名"

# Python MCP サーバー生成（mise + uv環境）
./scaffold python mcp-server file-manager author="開発者名"
```

### ⚡ Go開発 (`go`)

Goプロジェクトのためのサービスパターンテンプレート

```bash
# Goサービス生成（インターフェース + 実装 + テスト）
./scaffold go service UserService internal/services author="開発者名"
```

## 📁 設定ファイル構造

新しい階層構造では、`.scaffold/` ディレクトリ内にカテゴリ別の設定ファイルを配置します：

```
.scaffold/
├── csharp/
│   ├── .scaffold.toml     # C#テンプレート設定
│   └── templates/         # C#テンプレートファイル
├── python/
│   ├── .scaffold.toml     # Pythonテンプレート設定
│   └── templates/         # Python テンプレートファイル
│       ├── fastapi/       # FastAPI サービステンプレート
│       └── mcp-server/    # MCP サーバーテンプレート
├── web/
│   ├── .scaffold.toml     # Webテンプレート設定
│   └── templates/         # Webテンプレートファイル
├── devtools/
│   ├── .scaffold.toml     # 開発ツール設定
│   └── templates/         # 開発ツールテンプレート
├── ai/
│   ├── .scaffold.toml     # AI開発設定
│   └── templates/         # AI開発テンプレート
│       ├── cursorrules/   # Cursor AI 設定テンプレート
│       ├── mcp-server/    # TypeScript MCP サーバー
│       └── cursor-docs/   # Cursor セットアップドキュメント
└── go/
    ├── .scaffold.toml     # Go開発設定
    └── templates/         # Goテンプレートファイル
```

### 📁 マルチスキャフォールド統合

複数の`.scaffold`ディレクトリから設定を自動マージし、階層的なテンプレート管理を実現：

#### 設定ファイル検索順序

1. **カレントディレクトリ**: `.scaffold/` (最優先)
2. **ホームディレクトリ**: `~/.scaffold/` 
3. **設定ディレクトリ**: `~/.config/scaffold/` (最低優先)

#### 設定マージ動作

- 近いディレクトリの設定が遠いディレクトリの設定を上書き
- 同名テンプレートは最も近い`.scaffold`ディレクトリのものを使用
- テンプレートファイルも同様の優先順位で検索
- カテゴリは全ディレクトリから重複なしでマージ

### 設定例

```toml
[templates.my-template]
description = "カスタムテンプレートの説明"

required_args = [
    { name = "namespace", description = "名前空間" },
    { name = "name", description = "クラス名" }
]

optional_args = [
    { name = "author", default = "Generated", description = "作成者名" },
    { name = "date", default = "{{current_date}}", description = "作成日" }
]

files = [
    { source = "templates/my-template.cs", destination = "{{namespace}}/{{name}}.cs" }
]
```

## 🎯 テンプレート変数

### 特殊変数

- `{{current_date}}`: 現在の日付 (YYYY-MM-DD)
- `{{current_time}}`: 現在の時刻 (HH:MM:SS)
- `{{current_datetime}}`: 現在の日時 (YYYY-MM-DD HH:MM:SS)

### パス解決

- **source**: カテゴリディレクトリ内の `.scaffold.toml` ファイルからの相対パス
- **destination**: 実行時のカレントディレクトリからの相対パス

## 🛠️ 開発

### プロジェクト構造

```
scaffold/
├── main.go              # メインアプリケーション
├── main_test.go         # 統合機能のテスト
├── .mise.toml          # Go バージョン管理
├── .scaffold/          # カテゴリ別テンプレート設定
│   ├── csharp/         # C#/.NET テンプレート (6個)
│   ├── python/         # Python テンプレート (2個)
│   │   ├── fastapi/    # FastAPI サービステンプレート
│   │   └── mcp-server/ # Python MCP サーバーテンプレート
│   ├── web/            # Web開発テンプレート (2個)
│   ├── devtools/       # 開発ツールテンプレート (2個)
│   ├── ai/             # AI開発テンプレート (5個)
│   │   ├── cursorrules/    # Cursor AI設定 (5言語)
│   │   ├── mcp-server/     # TypeScript MCP サーバー
│   │   └── cursor-docs/    # Cursor セットアップドキュメント
│   └── go/             # Go開発テンプレート (1個)
├── .github/            # GitHub Actions ワークフロー
└── CLAUDE.md           # Claude Code 用ガイド
```

### テスト

```bash
# 従来のテンプレートテスト
./scaffold csharp usecase Application Users CreateUser
./scaffold web react-component TestComponent
./scaffold devtools makefile-advanced test-project

# 新しいAI統合テンプレートテスト
./scaffold ai claude-cursorrules react
./scaffold ai claude-mcp-server test-server typescript

# 新しいPythonテンプレートテスト
./scaffold python fastapi-service test-api test_api
./scaffold python mcp-server test-mcp

# 統合テスト
go test -v ./...
```

## 📚 利用可能なテンプレート

### 🏛️ C# (.NET) - 6個のテンプレート
- `usecase` - ユースケース実装 (Request/Response付き)
- `entity` - ドメインエンティティ
- `valueobject` - 値オブジェクト
- `repository` - リポジトリ (インターフェース + 実装)
- `exception` - ドメイン例外クラス
- `webapi-controller` - Web APIコントローラー

### 🐍 Python - 2個のテンプレート
- `fastapi-service` - FastAPI REST APIサービス (SQLAlchemy, 認証, テスト付き)
- `mcp-server` - Python MCP サーバー (mise + uv, 構造化ログ, 型安全)

### 🌐 Web開発 - 2個のテンプレート
- `react-component` - React TypeScriptコンポーネント
- `vite-react-ts` - Vite + React + TypeScript プロジェクト

### 🛠️ 開発ツール - 2個のテンプレート
- `makefile-advanced` - 高機能Makefile (自動ドキュメント生成)
- `github-actions-ci` - GitHub Actions CI/CDワークフロー

### 🤖 AI開発 - 5個のテンプレート
- `claude-cursorrules` - Cursor AI設定 (React, Python, Go, Rust, Node.js対応)
- `claude-mcp-server` - TypeScript MCP サーバー
- `claude-commands` - Claude Code カスタムコマンド
- `claude-project-init` - AI開発プロジェクト初期化
- `claude-multiagent` - マルチエージェント通信システム

### ⚡ Go開発 - 1個のテンプレート
- `service` - Goサービス (インターフェース + 実装 + テスト)

## 🌟 新機能ハイライト

### 🎯 AI統合テンプレート

#### Cursor AI統合
```bash
# 技術スタック別の.cursorrules生成
scaffold ai claude-cursorrules react     # React TypeScript用
scaffold ai claude-cursorrules python    # Python用
scaffold ai claude-cursorrules go        # Go用
scaffold ai claude-cursorrules rust      # Rust用
scaffold ai claude-cursorrules node      # Node.js用
```

#### MCP (Model Context Protocol) サーバー
```bash
# TypeScript MCP サーバー
scaffold ai claude-mcp-server file-manager typescript

# Python MCP サーバー (mise + uv)
scaffold python mcp-server database-connector
```

### 🐍 モダンPython開発

#### FastAPI マイクロサービス
```bash
# 完全なFastAPI サービス（認証、DB、テスト付き）
scaffold python fastapi-service user-api user_api database=postgresql auth=true
```

#### mise + uv 統合
- Python 3.12+ 対応
- uv による高速パッケージ管理
- mise による環境管理
- 構造化ログ（structlog）
- 完全な型安全性（mypy）

### 🔄 マルチスキャフォールド統合

複数の`.scaffold`ディレクトリからの自動設定マージにより：
- プロジェクト固有のカスタムテンプレート
- チーム共有テンプレート
- 個人用グローバルテンプレート

を同時に利用可能

## 🤝 コントリビューション

1. リポジトリをフォーク
2. フィーチャーブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

## 📄 ライセンス

このプロジェクトは MIT ライセンスの下で公開されています。詳細は [LICENSE](LICENSE) ファイルを参照してください。

## 🙏 謝辞

- [cobra](https://github.com/spf13/cobra) - 強力なCLIライブラリ
- [toml](https://github.com/BurntSushi/toml) - TOML設定ファイル解析
- [mise](https://mise.jdx.dev/) - ランタイムバージョン管理
- [nishimoto265/Claude-Code-Communication](https://github.com/nishimoto265/Claude-Code-Communication) - マルチエージェントシステムの参考実装
- [Zenn記事 by loglass](https://zenn.dev/loglass/articles/0016-make-makefile) - 高機能Makefileの設計参考