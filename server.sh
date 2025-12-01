#!/bin/bash

# 定义服务名称和相关路径
SERVICE_NAME="Sentinel"
PID_FILE="/tmp/${SERVICE_NAME}.pid"

# 获取服务状态
get_pid() {
    if [ -f "$PID_FILE" ]; then
        cat "$PID_FILE"
    fi
}

# 检查服务是否运行
is_running() {
    local pid=$(get_pid)
    if [ ! -z "$pid" ] && ps -p "$pid" > /dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# 启动服务
start() {
    if is_running; then
        echo "$SERVICE_NAME 服务已在运行中 (PID: $(get_pid))"
        return 1
    fi

    echo "更新服务依赖文件"
    uv sync > /dev/null 2>&1

    echo "正在启动 $SERVICE_NAME 服务..."

    # 直接启动 main.py
    uv run python main.py > /dev/null 2>&1 &

    local pid=$!
    echo $pid > "$PID_FILE"

    # 等待一会儿确认服务启动
    sleep 2

    if ps -p "$pid" > /dev/null 2>&1; then
        echo "$SERVICE_NAME 服务已成功启动 (PID: $pid)"
    else
        echo "$SERVICE_NAME 服务启动失败"
        rm -f "$PID_FILE"
        return 1
    fi
}

# 停止服务
stop() {
    if ! is_running; then
        echo "$SERVICE_NAME 服务未运行"
        return 1
    fi

    local pid=$(get_pid)
    echo "正在停止 $SERVICE_NAME 服务 (PID: $pid)..."

    kill "$pid"
    sleep 3

    # 如果还没停止，强制杀死
    if ps -p "$pid" > /dev/null 2>&1; then
        echo "强制终止服务..."
        kill -9 "$pid"
    fi

    rm -f "$PID_FILE"
    echo "$SERVICE_NAME 服务已停止"
}

# 查看服务状态
status() {
    if is_running; then
        local pid=$(get_pid)
        echo "$SERVICE_NAME 服务正在运行 (PID: $pid)"
    else
        echo "$SERVICE_NAME 服务未运行"
    fi
}

# 主命令处理
case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        stop
        sleep 2
        start
        ;;
    status)
        status
        ;;
    *)
        echo "用法: $0 {start|stop|restart|status}"
        exit 1
        ;;
esac

exit 0
