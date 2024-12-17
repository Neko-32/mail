## 使用方法
安裝 git
```bash
sudo apt install git
```  
使用 git 複製此儲存庫
```bash
git clone https://github.com/Neko-32/PiDoorNotifier.git
```  
安裝
```bash
chmod +x ./PiDoorNotifier/install.sh && ./PiDoorNotifier/install.sh
```  
執行
```bash
22-is-very-oily
```
附帶 -s 參數可以獲得驚喜  
```bash
22-is-very-oily -s
```
若遇到 400/401 錯誤，那應該是樹梅派內建的瀏覽器的問題，請改用 SSH 連線至樹梅派上的方式進行操作  

在 PowerShell 或 cmd 執行以下指令（在教室電腦上）
```powershell
ssh -L <port>:localhost:<port> <username>@<IP>
```
在樹梅派上執行 `whoami` 和 `hostname -I` 取得 `username` 及 `IP`  

`port` 處請輸入 1 ~ 65535 之間的任意整數，且 `:localhost:` 左右兩邊的數字必須是一樣的，例如：  
```powershell
ssh -L 8080:localhost:8080 pi@192.168.120.1
```
ssh 詳細請見：https://hackmd.io/@ncnu-opensource/1131-lsa-ssh （非必要）

![2tqz53ykkzoc1](https://github.com/user-attachments/assets/db82f439-e382-4ead-b998-f24824a8b7e5)  
最後這張圖只是附給那些說 Linux 爛的人看的
