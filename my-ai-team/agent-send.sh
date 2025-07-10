#!/bin/bash

# my-ai-team - Agent Communication Script
# Author: Test Developer
# Created: 2025-07-10
# Based on: https://github.com/nishimoto265/Claude-Code-Communication

# カラー出力用の関数
print_info() {
    echo -e "\033[1;34m[INFO]\033[0m $1"
}

print_success() {
    echo -e "\033[1;32m[SUCCESS]\033[0m $1"
}

print_error() {
    echo -e "\033[1;31m[ERROR]\033[0m $1"
}

# tmuxセッションのインデックスを取得する関数
get_session_index() {
    local session_name="$1"
    tmux list-sessions -F "#{session_name}" 2>/dev/null | grep -n "^${session_name}$" | cut -d: -f1
}

# エージェントからtmuxターゲットへのマッピング
get_agent_target() {
    local agent="$1"
    case "$agent" in
        "president")
            echo "president"
            ;;
        "boss1")
            echo "multiagent:main.0"
            ;;
        "worker1")
            echo "multiagent:main.1"
            ;;
        "worker2")
            echo "multiagent:main.2"
            ;;
        "worker3")
            echo "multiagent:main.3"
            ;;
        *)
            return 1
            ;;
    esac
}

# 使用方法を表示
show_usage() {
    echo "Usage: $0 [target-agent] [message]"
    echo "       $0 --list"
    echo "       $0 --help"
    echo ""
    echo "Examples:"
    echo "  $0 boss1 \"Hello from president\""
    echo "  $0 worker1 \"Start your task\""
    echo "  $0 --list"
}

# 利用可能なエージェントを表示
list_agents() {
    echo "Available agents:"
    echo "  president  - PRESIDENT (統括管理者)"
    echo "  boss1      - Team Leader (チームリーダー)"
    echo "  worker1    - Worker 1 (作業実行者1)"
    echo "  worker2    - Worker 2 (作業実行者2)"
    echo "  worker3    - Worker 3 (作業実行者3)"
    echo ""
    echo "Active tmux sessions:"
    tmux list-sessions 2>/dev/null || echo "  No active sessions found"
}

# メッセージ送信をログに記録
log_message() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local from_agent="$1"
    local to_agent="$2"
    local message="$3"
    echo "[$timestamp] $from_agent → $to_agent: $message" >> send.log
}

# エラーをログに記録
log_error() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local error_msg="$1"
    echo "[$timestamp] ERROR: $error_msg" >> error.log
}

# メッセージを送信
send_message() {
    local target_agent="$1"
    local message="$2"
    
    # ターゲットのtmuxセッション/ペインを取得
    local target=$(get_agent_target "$target_agent")
    if [ $? -ne 0 ]; then
        print_error "Unknown agent: $target_agent"
        log_error "Unknown agent: $target_agent"
        list_agents
        exit 1
    fi
    
    # tmuxセッションが存在するかチェック
    local session_name=$(echo "$target" | cut -d: -f1)
    if ! tmux has-session -t "$session_name" 2>/dev/null; then
        print_error "Session '$session_name' not found. Please run ./setup.sh first."
        log_error "Session '$session_name' not found"
        exit 1
    fi
    
    # メッセージを送信
    print_info "Sending message to $target_agent..."
    if tmux send-keys -t "$target" "$message" Enter; then
        print_success "Message sent to $target_agent successfully"
        log_message "system" "$target_agent" "$message"
    else
        print_error "Failed to send message to $target_agent"
        log_error "Failed to send message to $target_agent: $message"
        exit 1
    fi
}

# メイン処理
main() {
    # 引数チェック
    if [ $# -eq 0 ]; then
        show_usage
        exit 1
    fi
    
    case "$1" in
        "--help"|"-h")
            show_usage
            exit 0
            ;;
        "--list"|"-l")
            list_agents
            exit 0
            ;;
        *)
            if [ $# -ne 2 ]; then
                print_error "Invalid number of arguments"
                show_usage
                exit 1
            fi
            
            local target_agent="$1"
            local message="$2"
            
            # メッセージ送信
            send_message "$target_agent" "$message"
            ;;
    esac
}

# スクリプト実行
main "$@"