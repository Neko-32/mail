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
import sys

if os.name == 'nt':  # Windows系统
    import msvcrt
    def getch():
        return msvcrt.getch().decode('utf-8').upper()
else:  # Unix-like系统
    import termios
    import tty
    def getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch.upper()
from datetime import datetime
from colorama import init, Fore, Style

# 初始化 colorama
init()

# 取得當前時間並格式化為 [HH:MM] 形式
now = Fore.GREEN + datetime.now().strftime("[%H:%M]")+Style.RESET_ALL

# 添加必要的範圍
SCOPES = [
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.readonly'
]

# 定義檔案路徑
CREDENTIALS_PATH = os.path.join(os.path.dirname(__file__), 'credentials.json')
TOKEN_PATH = os.path.join(tempfile.gettempdir(), 'token.json')
ASCII_ART_PATH = os.path.join(os.path.dirname(__file__), 'takodachi.txt')


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
    redirect_uris = [
            "http://localhost",
        ]

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

def is_ssh_session():
    """檢測是否為 SSH 會話"""
    return 'SSH_CONNECTION' in os.environ or 'SSH_CLIENT' in os.environ
def get_gmail_service():
    """初始化 Gmail API 服務"""
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # 檢測是否為 SSH 會話
            if is_ssh_session():
                while True:
                    try:
                        port = input("請輸入用於 OAuth 驗證的端口 (預設為隨機)，必須與你在 ssh 連線時輸入的端口相同: ").strip()
                        port = int(port) if port else 0
                        
                        flow = InstalledAppFlow.from_client_secrets_file(
                            CREDENTIALS_PATH, SCOPES
                        )
                        creds = flow.run_local_server(
                            port=port,
                            open_browser=False,
                            authorization_prompt_message='請使用 Ctrl + 滑鼠左鍵開啟連結： {url}'
                        )
                        break
                    except ValueError:
                        print("無效的端口號，請輸入一個有效的整數")
                    except Exception as e:
                        print(f"連接埠 {port} 已被占用或發生錯誤：{e}")
                        sys.exit(1)
            else:
                # 本機執行，使用 port=0
                flow = InstalledAppFlow.from_client_secrets_file(
                    CREDENTIALS_PATH, SCOPES
                )
                creds = flow.run_local_server(
                    port=0,  # 自動選擇可用端口
                    open_browser=True,
                    authorization_prompt_message='請使用 Ctrl + 滑鼠左鍵開啟連結： {url}'
                )
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
        print(now + ' 郵件發送成功')
    except HttpError as error:
        print(Fore.RED + f'An error occurred: {error}' + Style.RESET_ALL)


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
            print("無效的輸入")
            cleanup()


if __name__ == '__main__':
    # ASCII art 來源：https://emojicombos.com/hololiveen
    # 打開文件並讀取內容
    with open(ASCII_ART_PATH, 'r', encoding='utf-8') as file:
        content = file.read()

    # 打印文件內容
    print(content)
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
        sys.exit(1)

    print("將使用 "+ Fore.LIGHTBLUE_EX + sender_email + Style.RESET_ALL + " 來發送郵件")

    recipient_email = input("請輸入收件人 Email: ").strip()

    print("程式啟動，此為測試模式，按下 1 以模擬 1 號門開啟，按下 2 以模擬 2 號門開啟，按下 Q 以結束程式")

    try:
        while True:
            time.sleep(0.001)
            #偵測使用者輸入
            user_input = getch().upper()

            if user_input == '1':
                print(now + " DOOR1 OPEN")
                send_email(gmail_service, sender_email, recipient_email, "1 號門已開啟", "DOOR1 OPEN")
                time.sleep(0.1)

            elif user_input == '2':
                print(now + " DOOR2 OPEN")
                send_email(gmail_service, sender_email, recipient_email, "2 號門已開啟", "DOOR2 OPEN")
                time.sleep(0.1)
            elif user_input == 'Q':
                print("程式結束")
                break

            else:
                print("無效的輸入")

    except KeyboardInterrupt:
        print("KeyboardInterrupt detected. Exiting...")

    finally:
        cleanup()
