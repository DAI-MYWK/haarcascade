import cv2
import smtplib
from email.mime.text import MIMEText

# Gmail 設定
sender_email = "送信元メールアドレス"
receiver_email = "送信先メールアドレス"
password = "Gmailのアプリパスワード"  # Gmailのアプリパスワード

# 顔検出器の初期化
face_cascade = cv2.CascadeClassifier('resources/haarcascade_frontalface_default.xml')

# メールを送信する関数
def send_email():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, password)
    msg = MIMEText('人間の姿が映りました')
    msg['Subject'] = 'Alert: Human Detected'
    msg['From'] = sender_email
    msg['To'] = receiver_email
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()
    print("Email sent!")

# カメラのキャプチャを開始
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    if len(faces) > 0:
        send_email()

    # 顔検出の結果を表示
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
    
    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # 'q' を押すとループから抜ける
        break

# リソースの解放
cap.release()
cv2.destroyAllWindows()
