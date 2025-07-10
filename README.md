# Universal Scaffold Tool

[![Go Version](https://img.shields.io/badge/Go-1.23+-blue.svg)](https://golang.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Universal Scaffold Tool は、様々な技術スタックに対応可能な汎用的なコード生成ツールです。Rails や Laravel のようなスキャフォールド機能を、あらゆるプロジェクトで利用できるようにすることを目的としています。

## 🚀 特徴

- **技術スタック非依存**: C#/.NET、React、Go など様々な言語・フレームワークに対応
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
# 利用可能なテンプレート一覧
./scaffold list

# テンプレートの詳細情報
./scaffold info [template-name]

# ファイル生成
./scaffold generate [template] [args...] [key=value...]
```

### C#/.NET テンプレート（DDD対応）

```bash
# ユースケース生成
./scaffold generate csharp-usecase Application Users CreateUser author="開発者名"

# ドメインエンティティ生成
./scaffold generate csharp-entity Domain Users User

# 値オブジェクト生成
./scaffold generate csharp-valueobject Domain Users Email

# リポジトリ生成（インターフェース + 実装）
./scaffold generate csharp-repository Domain Users User

# ドメイン例外クラス生成
./scaffold generate csharp-exception Domain Users EUS_001_001 UserNameRequired

# Web APIコントローラー生成
./scaffold generate csharp-webapi-controller Presentation Users User
```

### React TypeScript テンプレート

```bash
# Reactコンポーネント生成
./scaffold generate react-component UserProfile author="開発者名"
```

### Go サービステンプレート

```bash
# Goサービス生成
./scaffold generate go-service UserService users author="開発者名"
```

## 📁 設定ファイル

`.scaffold.toml` ファイルでテンプレートを定義します。以下の順序で検索されます：

1. カレントディレクトリの `.scaffold.toml`
2. ホームディレクトリの `~/.scaffold.toml`
3. 設定ディレクトリの `~/.config/scaffold/.scaffold.toml`

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

- **source**: `.scaffold.toml` ファイルからの相対パス
- **destination**: 実行時のカレントディレクトリからの相対パス


## 🛠️ 開発

### プロジェクト構造

```
scaffold/
├── main.go              # メインアプリケーション
├── .scaffold.toml       # テンプレート設定
├── .mise.toml          # Go バージョン管理
├── templates/          # テンプレートファイル
│   ├── csharp/         # C#/.NET テンプレート
│   ├── react/          # React テンプレート
│   ├── go/             # Go テンプレート
│   └── mvc/            # ASP.NET MVC テンプレート
└── CLAUDE.md           # Claude Code 用ガイド
```

### テスト

```bash
# テスト用ディレクトリでテンプレート生成をテスト
mkdir test && cd test
cp ../.scaffold.toml .
cp -r ../templates .
../scaffold generate csharp-usecase Application Users CreateUser
```


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