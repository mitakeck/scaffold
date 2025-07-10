#!/bin/bash

# {{name}} - Multi-Agent Communication Demo Environment Setup
# Author: {{author}}
# Created: {{date}}
# Based on: https://github.com/nishimoto265/Claude-Code-Communication

# カラー出力用の関数
print_info() {
    echo -e "\033[1;34m[INFO]\033[0m $1"
}

print_success() {
    echo -e "\033[1;32m[SUCCESS]\033[0m $1"
}

print_warning() {
    echo -e "\033[1;33m[WARNING]\033[0m $1"
}

print_error() {
    echo -e "\033[1;31m[ERROR]\033[0m $1"
}

print_header() {
    echo -e "\033[1;36m"
    echo "=================================================="
    echo "🤖 {{name}} Setup"
    echo "Multi-Agent Communication Demo Environment"
    echo "=================================================="
    echo -e "\033[0m"
}

# エラーハンドリング
set -e
trap 'print_error "Setup failed at line $LINENO"' ERR

print_header

# 既存のセッションをクリーンアップ
print_info "Cleaning up existing tmux sessions..."
tmux kill-session -t multiagent 2>/dev/null || true
tmux kill-session -t president 2>/dev/null || true

# 必要なディレクトリを作成
print_info "Creating necessary directories..."
mkdir -p tmp
mkdir -p logs

# multiagentセッションの作成（boss1 + {{workers}} workers）
print_info "Creating multiagent session with {{workers}} workers..."
tmux new-session -d -s multiagent -n main

# ペインを分割（4つのペイン: boss1, worker1, worker2, worker3）
tmux split-window -h -t multiagent:main
tmux split-window -v -t multiagent:main.0
tmux split-window -v -t multiagent:main.2

# 各ペインにカスタムプロンプトとカラーを設定
print_info "Configuring agent environments..."

# boss1 (ペイン0) - 青背景
tmux send-keys -t multiagent:main.0 'export PS1="\[\033[1;37;44m\][boss1]\[\033[0m\] \w $ "' Enter
tmux send-keys -t multiagent:main.0 'echo "🎯 boss1 environment ready"' Enter
tmux send-keys -t multiagent:main.0 'echo "Instructions: cat instructions/boss.md"' Enter

# worker1 (ペイン1) - 緑背景  
tmux send-keys -t multiagent:main.1 'export PS1="\[\033[1;37;42m\][worker1]\[\033[0m\] \w $ "' Enter
tmux send-keys -t multiagent:main.1 'echo "👷 worker1 environment ready"' Enter
tmux send-keys -t multiagent:main.1 'echo "Instructions: cat instructions/worker.md"' Enter

# worker2 (ペイン2) - 黄背景
tmux send-keys -t multiagent:main.2 'export PS1="\[\033[1;37;43m\][worker2]\[\033[0m\] \w $ "' Enter
tmux send-keys -t multiagent:main.2 'echo "👷 worker2 environment ready"' Enter
tmux send-keys -t multiagent:main.2 'echo "Instructions: cat instructions/worker.md"' Enter

# worker3 (ペイン3) - マゼンタ背景
tmux send-keys -t multiagent:main.3 'export PS1="\[\033[1;37;45m\][worker3]\[\033[0m\] \w $ "' Enter
tmux send-keys -t multiagent:main.3 'echo "👷 worker3 environment ready"' Enter
tmux send-keys -t multiagent:main.3 'echo "Instructions: cat instructions/worker.md"' Enter

# presidentセッションの作成
print_info "Creating president session..."
tmux new-session -d -s president
tmux send-keys -t president 'export PS1="\[\033[1;37;41m\][PRESIDENT]\[\033[0m\] \w $ "' Enter
tmux send-keys -t president 'echo "👑 PRESIDENT environment ready"' Enter
tmux send-keys -t president 'echo "Instructions: cat instructions/president.md"' Enter

print_success "Environment setup completed!"

print_info "Next steps:"
echo "1. Connect to president session: tmux attach-session -t president"
echo "2. Connect to multiagent session: tmux attach-session -t multiagent"
echo "3. In each session, authenticate with Claude Code"
echo "4. Start the demo by telling PRESIDENT: 'あなたはpresidentです。指示書に従って'"
echo ""
print_info "Available commands:"
echo "• ./agent-send.sh --list           # List available agents"
echo "• ./agent-send.sh [agent] [message] # Send message to agent"
echo "• tmux list-sessions               # Show active sessions"
echo ""
print_warning "Make sure to authenticate with Claude Code in each tmux pane before starting!"

# ログファイルの初期化
touch send.log error.log
print_info "Log files initialized: send.log, error.log"

print_success "🎉 {{name}} environment is ready!"