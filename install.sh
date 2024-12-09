#!/bin/bash

# 安裝 Python 依賴項
pip3 install --upgrade google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client

# 獲取當前腳本所在目錄
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)

# 目標目錄
TARGET_DIR="/usr/local/bin"

# 檢查目標目錄是否存在，如果不存在則創建
if [ ! -d "$TARGET_DIR" ]; then
    echo "目標目錄不存在，正在創建：$TARGET_DIR"
    sudo mkdir -p "$TARGET_DIR"
fi

# 移動 PiDoorGmail 目錄
if [ -d "$SCRIPT_DIR/PiDoorGmail" ]; then
    echo "正在移動 PiDoorGmail 到 $TARGET_DIR..."
    sudo mv "$SCRIPT_DIR/PiDoorGmail" "$TARGET_DIR"
else
    echo "警告：PiDoorGmail 目錄未找到！"
fi

# 移動 22_is_very_oily 腳本
if [ -f "$SCRIPT_DIR/22_is_very_oily" ]; then
    echo "正在移動 22_is_very_oily 到 $TARGET_DIR..."
    sudo mv "$SCRIPT_DIR/22_is_very_oily" "$TARGET_DIR"
else
    echo "警告：22_is_very_oily 腳本未找到！"
fi

echo "操作完成！"