import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Gmail 配置
sender_email = "021021hxc@gmail.com"
receiver_email = "24028069d@connect.polyu.hk"   # 正确写法
app_password = "zatknjnalkvknepy"               # 应用专用密码，去掉空格

# 构建邮件
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = "测试邮件 - Gmail Python"

body = "你好，这是通过 Gmail + Python 发送的测试邮件。"
message.attach(MIMEText(body, "plain"))

try:
    # 连接 Gmail SMTP
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, app_password)
    server.sendmail(sender_email, receiver_email, message.as_string())
    server.quit()
    print("✅ 邮件发送成功！")
except Exception as e:
    print("❌ 邮件发送失败:", e)
