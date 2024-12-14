#!/bin/bash
sudo apt install curl -y || sudo apt install curl --fix-missing -y
# 安裝 Python 依賴項
pip3 install --upgrade google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client colorama
if [ $? -ne 0 ]; then
    echo "Python 依賴項安裝失敗，請檢查錯誤信息。"
fi

# 獲取當前腳本所在目錄
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)

# 目標目錄
TARGET_DIR="/usr/local/bin"

# 檢查目標目錄是否存在，如果不存在則創建
if [ ! -d "$TARGET_DIR" ]; then
    echo "目標目錄不存在，正在創建：$TARGET_DIR"
    sudo mkdir -p "$TARGET_DIR"
fi

# 標誌變量
SUCCESS=true

# 移動 PiDoorGmail 目錄
if [ -d "$SCRIPT_DIR/PiDoorGmail" ]; then
    echo "正在複製 PiDoorGmail 到 $TARGET_DIR..."
    sudo cp -r "$SCRIPT_DIR/PiDoorGmail" "$TARGET_DIR"
else
    echo "警告：PiDoorGmail 目錄未找到！"
    SUCCESS=false
fi

# 移動 22-is-very-oily 腳本
if [ -f "$SCRIPT_DIR/22-is-very-oily" ]; then
    echo "正在複製 22-is-very-oily 到 $TARGET_DIR..."
    sudo cp "$SCRIPT_DIR/22-is-very-oily" "$TARGET_DIR"
    sudo chmod +x "$TARGET_DIR/22-is-very-oily"
else
    echo "警告：22-is-very-oily 腳本未找到！"
    SUCCESS=false
fi

# 根據標誌變量輸出結果
if [ "$SUCCESS" = true ]; then
    echo "安裝完成！輸入 22-is-very-oily 以執行此程式"
else
    echo "安裝過程中出現錯誤，請檢查上面的警告信息。"
fi
