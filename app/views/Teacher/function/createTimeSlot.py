from typing import List
from fastapi import APIRouter, Depends, Form, Request
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.DBconnection import get_db 
import random, string
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List
import os

SMTP_HOST = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("EMAIL_USER")
SMTP_PASS = os.getenv("EMAIL_PASS")
SMTP_FROM = os.getenv("SMTP_FROM", SMTP_USER)
SMTP_FROM_NAME = os.getenv("SMTP_FROM_NAME", "FastAPI Service")


router = APIRouter()

def generate_password():
    digits = ''.join(random.choices(string.digits, k=3))
    letters = ''.join(random.choices(string.ascii_letters, k=3))  # 大小寫混合
    return digits + letters

    
@router.post("/createTimeSlot")
async def create_time_slot(
    request: Request,
    title: str = Form(...),
    start: List[str] = Form(...),   # 多個 start[]
    end: List[str] = Form(...),     # 多個 end[]
    status: str = Form("Available"),
    content: str = Form(None),
    capacity: int = Form(...),
    deadline: str  = Form(...),
    students: List[str] = Form([]),
    db: Session = Depends(get_db)
):
    teacher_id = request.cookies.get("user_id")
    if not teacher_id:
        return {"error": "teacher_id not found in cookie"}

    # 1️⃣ 先檢查所有 slot 是否衝突
    for i in range(len(start)):
        s = start[i]
        e = end[i]

        check_stmt = text("""
            SELECT 1 FROM booking_time_slot
            WHERE teacher_id = :teacher_id
              AND (start < :end AND end > :start)
            LIMIT 1
        """)
        conflict = db.execute(check_stmt, {
            "teacher_id": teacher_id,
            "start": s,
            "end": e
        }).fetchone()

        if conflict:
            return {"message": f"Time slot conflicts with existing schedule (start={s}, end={e})"}

    # 2️⃣ 生成唯一 group_id
    while True:
        letters = ''.join(random.choices(string.ascii_uppercase, k=4))  # 4 個大寫字母
        numbers = ''.join(random.choices(string.digits, k=6))           # 6 位數字
        group_id = letters + numbers

        check_stmt = text("SELECT 1 FROM booking_time_slot WHERE timeSlotGroupId = :gid LIMIT 1")
        exists = db.execute(check_stmt, {"gid": group_id}).fetchone()
        if not exists:
            break  # 確保唯一

    # 3️⃣ 沒有衝突 → 批量插入，全部用同一個 group_id
    for i in range(len(start)):
        insert_stmt = text("""
            INSERT INTO booking_time_slot 
                (title, timeSlotGroupId, start, end, status, teacher_id, content, capacity, vacancy,deadline)
            VALUES 
                (:title, :gid, :start, :end, :status, :teacher_id, :content, :capacity, :vacancy,:deadline)
        """)
        db.execute(insert_stmt, {
            "title": title,
            "gid": group_id,
            "start": start[i],
            "end": end[i],
            "status": status,
            "teacher_id": teacher_id,
            "content": content,
            "capacity": capacity,
            "vacancy":capacity,
            "deadline": deadline
        })

    for sid in students:
        email = f"{sid}@connect.polyu.hk"

        # 檢查 user 是否存在
        user_row = db.execute(
            text("SELECT id, password FROM users WHERE email = :email"),
            {"email": email}
        ).fetchone()

        if not user_row:
            password = generate_password()
            db.execute(text("""
                INSERT INTO users (email, password, full_name, role_id, created_at, updated_at)
                VALUES (:email, :password, '', :role_id, NOW(), NOW())
            """), {
                "email": email,
                "password": password,
                "role_id": 1  # student
            })
            user_row = db.execute(
                text("SELECT id FROM users WHERE email = :email"),
                {"email": email}
            ).fetchone()

            send_timeslot_email(
            recipient=email,
            password=password,
            title=title,
            start_list=start,
            end_list=end,
            deadline=deadline,
            content=content or ""
            )
        else:
            send_timeslot_email(
            recipient=email,
            password=user_row.password,  # 空字串代表不顯示
            title=title,
            start_list=start,
            end_list=end,
            deadline=deadline,
            content=content or ""
            )

        user_id = user_row.id

        # 插入 group-student 關聯
        db.execute(text("""
            INSERT INTO time_slot_group_student (group_id, user_id)
            VALUES (:gid, :uid)
        """), {"gid": group_id, "uid": user_id})

    db.commit()

    return {
        "message": "All time slots and students created successfully",
        "timeSlotGroupId": group_id
    }

    
def send_timeslot_email(
    recipient: str,
    password: str,
    title: str,
    start_list: List[str],
    end_list: List[str],
    deadline: str,
    content: str = ""
):
    """
    發送時段建立通知郵件
    recipient: 學生 email
    password: 初始密碼（新建立的帳號才需要，已存在帳號可傳空字串）
    title: 時段標題
    start_list: 時段開始時間列表
    end_list: 時段結束時間列表
    deadline: 預約截止時間
    content: 額外說明
    """
    try:
        msg = MIMEMultipart("alternative")
        msg["From"] = f"{SMTP_FROM_NAME} <{SMTP_FROM}>"
        msg["To"] = recipient
        msg["Subject"] = f"[Booking Notice] {title}"

        # 格式化時段列表
        slot_info = ""
        for s, e in zip(start_list, end_list):
            slot_info += f"<li>{s} → {e}</li>\n"

        # 郵件文字內容
        text_content = f"""
        You have been added to the booking group: {title}
        Deadline: {deadline}
        {content if content else ""}
        
        Available time slots:
        {', '.join([f"{s} - {e}" for s, e in zip(start_list, end_list)])}
        
        {"Your temporary password is: " + password if password else ""}
        """

        html_content = f"""
        <p>You have been added to the booking group: <b>{title}</b></p>
        <p><b>Deadline:</b> {deadline}</p>
        <p>{content if content else ""}</p>
        <p>Available time slots:</p>
        <ul>
            {slot_info}
        </ul>
        {f"<p><b>Your temporary password:</b> {password}</p>" if password else ""}
        """

        msg.attach(MIMEText(text_content, "plain"))
        msg.attach(MIMEText(html_content, "html"))

        # 發送郵件
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_FROM, recipient, msg.as_string())

        print(f"📩 Mail sent to {recipient}")

    except Exception as e:
        print(f"❌ Failed to send mail to {recipient}: {e}")