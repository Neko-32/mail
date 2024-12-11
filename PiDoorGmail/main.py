from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.text import MIMEText
import base64
import json
import os
import tempfile
import time
import RPi.GPIO as GPIO
import sys
import termios
import tty
import webbrowser
import subprocess
def open_browser(url):
    try:
        # 方法1：使用 webbrowser 模組
        webbrowser.open(url)
    except Exception as e:
        try:
            # 方法2：使用 xdg-open（在大多數 Linux 系統，包括樹莓派）
            subprocess.run(['xdg-open', url], check=True)
        except Exception as e2:
            try:
                # 方法3：直接指定常見瀏覽器
                browsers = [
                    'chromium-browser',
                    'google-chrome',
                    'firefox',
                    'x-www-browser'
                ]
                
                for browser in browsers:
                    try:
                        subprocess.run([browser, url], check=True)
                        break
                    except:
                        continue
            except Exception as e3:
                print(f"無法開啟瀏覽器。錯誤：{e3}，請自行複製網址在瀏覽器打開")

def getch():
    """讀取單個字符而不需要按 Enter"""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

# 添加必要的範圍
SCOPES = [
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.readonly'
]

# 定義檔案路徑
CREDENTIALS_PATH = os.path.join(os.path.dirname(__file__), 'credentials.json')
TOKEN_PATH = os.path.join(tempfile.gettempdir(), 'token.json')


def ask_to_delete_token():
    """詢問用戶是否刪除 token.json"""
    if os.path.exists(TOKEN_PATH):
        delete = input(f"要使用上次登入的帳戶來發送郵件嗎？(Y/N): ").strip().upper()
        if delete == 'N':
            os.remove(TOKEN_PATH)
            print(f"已刪除 {TOKEN_PATH}，請重新登入")
        elif delete != 'Y':
            print("無效的輸入，請輸入 Y 或 N")
            ask_to_delete_token()

def ask_user_for_credentials():
    """動態輸入 client_id 和 client_secret 並生成 credentials.json"""
    print("請輸入 Google API 的客戶端資訊：")
    client_id = input("Client ID: ").strip()
    client_secret = input("Client Secret: ").strip()
    redirect_uris = ["http://localhost"]

    credentials_data = {
        "installed": {
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uris": redirect_uris,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token"
        }
    }

    with open(CREDENTIALS_PATH, 'w') as cred_file:
        json.dump(credentials_data, cred_file, indent=4)

    print(f"已生成 {CREDENTIALS_PATH} 檔案！")


def get_gmail_service():
    """初始化 Gmail API 服務"""
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())
    try:
        service = build('gmail', 'v1', credentials=creds)
        return service
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None


def get_sender_email(service):
    """通過 API 獲取寄件人 Email"""
    try:
        profile = service.users().getProfile(userId="me").execute()
        return profile['emailAddress']
    except HttpError as error:
        print(f"An error occurred while fetching sender email: {error}")
        return None


def create_message(sender, to, subject, message_text):
    """創建 MIME 格式的郵件"""
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw_message}


def send_email(service, sender, to, subject, message_text):
    """發送郵件"""
    try:
        message = create_message(sender, to, subject, message_text)
        sent_message = service.users().messages().send(userId="me", body=message).execute()
        print(f'郵件發送成功')
    except HttpError as error:
        print(f'An error occurred: {error}')


def cleanup():
    """結束時詢問用戶是否刪除 token.json"""
    if os.path.exists(TOKEN_PATH):
        delete = input(f"程式結束，是否要保留 Token 以省略之後的登入流程？(Y/N): ").strip().upper()
        if delete == 'N':
            os.remove(TOKEN_PATH)
            print(f"已刪除 Token，下次需要重新登入\n程式結束")
        elif delete == 'Y':
            print("已保留 Token，下次可以直接使用\n程式結束")
        else:
            print("無效的輸入，請輸入 Y 或 N")
            cleanup()


if __name__ == '__main__':
    # 問是否刪除舊的 token.json
    ask_to_delete_token()

    # 檢查是否需要生成 credentials.json
    if not os.path.exists(CREDENTIALS_PATH):
        ask_user_for_credentials()
    gmail_service = get_gmail_service()

    # 獲取寄件人 Email
    sender_email = get_sender_email(gmail_service)
    if not sender_email:
        print("無法獲取寄件人 Email，程式結束。")
        cleanup()
        exit(1)

    print(f"將使用 {sender_email} 來發送郵件")

    recipient_email = input("請輸入收件人 Email: ").strip()

    print("程式啟動，按 I 更改收件人信箱，按 Q 結束。")

    try:
        while True:
            time.sleep(0.001)

            if GPIO.input(S1) == 0 and S1_buffer == 1:
                print("DOOR1 OPEN")
                send_email(gmail_service, sender_email, recipient_email, "1 號門已開啟", "DOOR1 OPEN")
                time.sleep(0.1)
            S1_buffer = GPIO.input(S1)

            if GPIO.input(S2) == 0 and S2_buffer == 1:
                print("DOOR2 OPEN")
                send_email(gmail_service, sender_email, recipient_email, "2 號門已開啟", "DOOR2 OPEN")
                time.sleep(0.1)
            S2_buffer = GPIO.input(S2)

            # 偵測使用者輸入
            user_input = getch().upper()

            if user_input == 'Q':
                break
            elif user_input == 'I':
                recipient_email = input("收件人 Email: ").strip()
            else:
                print("無效的輸入，請輸入 I 或 Q。")

    except KeyboardInterrupt:
        print("KeyboardInterrupt detected. Exiting...")

    finally:
        cleanup()