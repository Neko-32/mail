## 使用方法

在 cmd 執行以下指令（Windows）
```powershell
ssh -L <port>:localhost:<port> <username>@<IP>
```
`port`（端口） 處請輸入 1 ~ 65535 之間的任意整數，且 `:localhost:` 左右兩邊的數字必須是一樣的，例如：  
```powershell
ssh -L 8080:localhost:8080 pi@192.168.120.1
```

安裝 git & 使用 git 複製此儲存庫 & 安裝（複製貼上就對了）
```bash
sudo apt install git && git clone https://github.com/Neko-32/PiDoorNotifier.git && chmod +x ./PiDoorNotifier/install.sh && ./PiDoorNotifier/install.sh
```  

執行
```bash
22-is-very-oily
```
附帶 -s 參數可以獲得驚喜（某些機器好像看不了）  
```bash
22-is-very-oily -s
```
