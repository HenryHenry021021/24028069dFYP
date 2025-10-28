from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime
from app.DBconnection import get_db 
import pytz
from app.websocket_manager import broadcast
tz = pytz.timezone("Asia/Hong_Kong")
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

SMTP_HOST = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("EMAIL_USER")
SMTP_PASS = os.getenv("EMAIL_PASS")
SMTP_FROM = os.getenv("SMTP_FROM", SMTP_USER)
SMTP_FROM_NAME = os.getenv("SMTP_FROM_NAME", "FastAPI Service")
router = APIRouter()

@router.post("/reserveTimeSlot")
async def book_slot(payload: dict, request: Request, db: Session = Depends(get_db)):
    student_id = request.cookies.get("user_id")
    group_id = payload.get("group_id")
    preference_list = payload.get("slot_id", [])  # 這裡是 list
    preference_list = [int(x) for x in preference_list if str(x).isdigit()]

    print("🟢 Received booking request:")
    print(f"  Student ID: {student_id}")
    print(f"  Group ID: {group_id}")
    print(f"  Preference List: {preference_list}")

    if not student_id or not group_id or not preference_list:
        return {"error": "缺少 student_id、group_id 或 preference_list"}

    stmt_check = text("""
                SELECT 1
                FROM students_booking
                WHERE student_id = :sid
                AND time_slot_id IN :preference_list
                LIMIT 1
            """)
    booked = db.execute(stmt_check, {
        "sid": student_id,
        "preference_list": tuple(preference_list)   # 必須轉成 tuple 才能給 IN (...)
    }).fetchone()

    if booked:
        return {"error": "您已經在這個 group 預約過，不能重複預約"}

    try:
        # ✅ 1️⃣ 先檢查該 group 的所有 slot
        stmt_slots = text("""
            SELECT id, vacancy
            FROM booking_time_slot
            WHERE timeSlotGroupId = :gid
            FOR UPDATE
        """)
        slot_rows = db.execute(stmt_slots, {"gid": group_id}).fetchall()

        if not slot_rows:
            return {"error": "找不到此 group 的任何時段"}

       
        # 轉成 dict {slot_id: vacancy}
        slot_map = {row.id: row.vacancy for row in slot_rows}

        print(slot_map)
        # ✅ 2️⃣ 依序嘗試預約 preference list 中的 slot
        for slot_id in preference_list:
            if slot_id not in slot_map:
                continue  # 該 slot 不在這個 group 內

            vacancy = slot_map[slot_id]
            if vacancy <= 0:
                continue  # 沒空位，換下一個

            # ✅ 有空位：先更新 vacancy
            stmt_update = text("""
                UPDATE booking_time_slot
                SET vacancy = vacancy - 1
                WHERE id = :slot_id AND vacancy > 0
            """)
            result = db.execute(stmt_update, {"slot_id": slot_id})

            if result.rowcount > 0:
                # ✅ 3️⃣ 插入 booking 紀錄
                stmt_insert = text("""
                    INSERT INTO students_booking (student_id, time_slot_id, created_at, status)
                    VALUES (:student_id, :slot_id, :created_at, 'Booked')
                """)
                db.execute(stmt_insert, {
                    "student_id": student_id,
                    "slot_id": slot_id,
                    "created_at": datetime.now(tz)
                })

                db.commit()

                print(f"✅ Booking success at slot_id = {slot_id}")
                send_booking_success_email(db, student_id, slot_id)
                return {"success": True, "slot_id": slot_id}

        # ❌ 若所有 slot 都沒有空位
        db.rollback()
        return {"error": "所有偏好時段均已滿"}

    except Exception as e:
        db.rollback()
        print("❌ Error:", e)
        return {"error": str(e)}

def send_booking_success_email(db: Session, student_id: int, time_slot_id: int):
    # 查學生 email
    student_row = db.execute(
        text("SELECT email FROM users WHERE id = :sid"),
        {"sid": student_id}
    ).fetchone()

    # 查 slot 資訊
    slot_row = db.execute(
        text("SELECT title, start, end, content FROM booking_time_slot WHERE id = :slot_id"),
        {"slot_id": time_slot_id}
    ).fetchone()

    # 📩 只用 HTML 郵件
    html_content = f"""
    <p>Your booking is <b>confirmed ✅</b></p>
    <ul>
        <li><b>Title:</b> {slot_row.title}</li>
        <li><b>Time:</b> {slot_row.start} → {slot_row.end}</li>
        <li><b>Content:</b> {slot_row.content or 'N/A'}</li>
    </ul>
    """

    msg = MIMEText(html_content, "html")
    msg["From"] = f"{SMTP_FROM_NAME} <{SMTP_FROM}>"
    msg["To"] = student_row.email
    msg["Subject"] = f"[Booking Success] {slot_row.title}"

    # 發送
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(SMTP_FROM, student_row.email, msg.as_string())

    print(f"📩 Booking success email sent to {student_row.email}")


