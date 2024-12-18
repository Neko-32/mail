## 使用方法

由於在樹梅派內建的瀏覽器進行 OAuth 驗證時會出現錯誤，因此改用 SSH 連線，在教室電腦上進行驗證  

在 cmd 執行以下指令，端口處請改成 1 ~ 65535 內的任意整數，且左右兩邊必須一樣
```
ssh -L 端口:localhost:端口 pi@你樹梅派的IP
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

詳細請見：
  - [絶対強者の殿堂へ：Linux 領域展開！](https://youtu.be/1oV5tCH5raY)
  - [SSH 遠端連線 - HackMD](https://hackmd.io/@jiazheng/ByLzJIvlkl)
  - [Gmail API 總覽](https://developers.google.com/gmail/api/guides?hl=zh-tw)

![image](https://raw.githubusercontent.com/Neko-32/Neko-32/refs/heads/main/396451274-db82f439-e382-4ead-b998-f24824a8b7e5.png)  
最後這張圖只是附給那些說 Linux 爛的人看的
