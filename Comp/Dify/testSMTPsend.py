import smtplib
from email.mime.text import MIMEText

# 送信元・送信先
from_addr = "your_address@gmail.com"
to_addr = "target@example.com"

# メールの内容
msg = MIMEText("メールの本文です")
msg["Subject"] = "テストメール"
msg["From"] = from_addr
msg["To"] = to_addr

# Gmail SMTP
smtp_server = "34.187.250.95"
smtp_port = 1025

# Gmailアプリパスワードを使用
password = "アプリパスワード"

with smtplib.SMTP(smtp_server, smtp_port) as server:
    #server.starttls()
    #server.login(from_addr, password)
    server.send_message(msg)

print("送信完了")
