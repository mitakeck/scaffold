# Universal Scaffold Tool

[![Go Version](https://img.shields.io/badge/Go-1.23+-blue.svg)](https://golang.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Universal Scaffold Tool は、様々な技術スタックに対応可能な汎用的なコード生成ツールです。Rails や Laravel のようなスキャフォールド機能を、あらゆるプロジェクトで利用できるようにすることを目的としています。

## 🚀 特徴

- **技術スタック非依存**: C#/.NET、React、Go など様々な言語・フレームワークに対応
- **カテゴリ別組織化**: テンプレートを目的別にカテゴリ分けして管理
- **テンプレートベース**: プレーンテキストファイルを使用した柔軟なテンプレート管理
- **TOML設定**: シンプルで読みやすい設定ファイル形式
- **変数展開**: `{{variable}}` 形式での動的コンテンツ生成
- **ディレクトリ自動作成**: 必要なディレクトリ構造を自動で作成
- **上書き保護**: 既存ファイルの上書き確認機能

## 📦 インストール

### 必要要件

- Go 1.23+
- [mise](https://mise.jdx.dev/) (推奨)

### ビルド方法

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

Claude Codeを活用したAI開発プロジェクトのテンプレート群

```bash
# Claude Code カスタムコマンド生成
./scaffold ai claude-commands refactor "Code refactoring assistant"

# AI開発プロジェクト初期化
./scaffold ai claude-project-init my-ai-project

# Claude Code マルチエージェント通信システム
./scaffold ai claude-multiagent my-team-project
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
├── web/
│   ├── .scaffold.toml     # Webテンプレート設定
│   └── templates/         # Webテンプレートファイル
├── devtools/
│   ├── .scaffold.toml     # 開発ツール設定
│   └── templates/         # 開発ツールテンプレート
├── ai/
│   ├── .scaffold.toml     # AI開発設定
│   └── templates/         # AI開発テンプレート
└── go/
    ├── .scaffold.toml     # Go開発設定
    └── templates/         # Goテンプレートファイル
```

### 設定ファイル検索順序

1. カレントディレクトリの `.scaffold/`
2. ホームディレクトリの `~/.scaffold/`
3. 設定ディレクトリの `~/.config/scaffold/`

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
├── .mise.toml          # Go バージョン管理
├── .scaffold/          # カテゴリ別テンプレート設定
│   ├── csharp/         # C#/.NET テンプレート
│   ├── web/            # Web開発テンプレート
│   ├── devtools/       # 開発ツールテンプレート
│   ├── ai/             # AI開発テンプレート
│   └── go/             # Go開発テンプレート
├── .github/            # GitHub Actions ワークフロー
└── CLAUDE.md           # Claude Code 用ガイド
```

### テスト

```bash
# 特定のカテゴリのテンプレートをテスト
./scaffold csharp usecase Application Users CreateUser
./scaffold web react-component TestComponent
./scaffold devtools makefile-advanced test-project
```

## 📚 利用可能なテンプレート

### C# (.NET) - 6個のテンプレート
- `usecase` - ユースケース実装 (Request/Response付き)
- `entity` - ドメインエンティティ
- `valueobject` - 値オブジェクト
- `repository` - リポジトリ (インターフェース + 実装)
- `exception` - ドメイン例外クラス
- `webapi-controller` - Web APIコントローラー

### Web開発 - 2個のテンプレート
- `react-component` - React TypeScriptコンポーネント
- `vite-react-ts` - Vite + React + TypeScript プロジェクト

### 開発ツール - 2個のテンプレート
- `makefile-advanced` - 高機能Makefile (自動ドキュメント生成)
- `github-actions-ci` - GitHub Actions CI/CDワークフロー

### AI開発 - 3個のテンプレート
- `claude-commands` - Claude Code カスタムコマンド
- `claude-project-init` - AI開発プロジェクト初期化
- `claude-multiagent` - マルチエージェント通信システム

### Go開発 - 1個のテンプレート
- `service` - Goサービス (インターフェース + 実装 + テスト)

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