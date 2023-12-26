#!/bin/bash

# 欲部署的分支
branch_name=$1

# 檢查有沒有輸入分之名稱
if [ -z "$branch_name" ]; then
    echo "沒有輸入分支"
    exit 1
fi

# 切換到 bookmazon git 資料夾
cd ~/app/bookmazon

# 切換到指定分支
git checkout "$branch_name"

# 從 remote repository 拉分支下來
# SSH 連線去拉分支，要先把伺服器的公鑰放到 Gitlab
git pull

# 找到佔用 8000 port 的 PID
pid=$(lsof -t -i:8000)

# 看有沒有 佔用 8000 port 的 PID
if [ -z "$pid" ]; then
    echo "沒有找到佔用 8000 port 的 PID"
else
    # 停止 Flask Web Server
    kill -15 "$pid"
    echo "停止 Flask Web Server: $pid"
fi

# 設定環境變數 FLASK_ENV 測試環境 test
export FLASK_ENV=test
# 啟動 Flask Web Server
gunicorn -w 1 -b 0.0.0.0 main:app --daemon

