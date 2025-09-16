from fastapi import APIRouter, Depends, Request
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.DBconnection import get_db 
router = APIRouter()

@router.get("/getTimeSlot")
async def get_events(teacher_id: int, request: Request, db: Session = Depends(get_db)):
    # 这就是 prepared statement
    user_id = request.cookies.get("user_id")

    stmt = text("""
        SELECT *
        FROM booking_time_slot
        WHERE teacher_id = :teacher_id
        ORDER BY start ASC
    """)

    result = db.execute(stmt, {"teacher_id": teacher_id}).mappings().all()
    events = []

    for r in result:
        # ✅ 默认荧光绿
        color = "#d4edda"        # ✅ 淡绿色背景 (Bootstrap success)
        border_color = "#28a745" # 亮绿色边框
        text_color = "#155724"   # 深绿色字体
        canBook = True
        # ❌ 如果不是 Available，就变灰色
        if r["status"] != "Available":
            color = "#e9ecef"        # 灰底
            border_color = "#ced4da" # 浅灰边框
            text_color = "#6c757d"   # 深灰字
            canBook = False

        if user_id:
            stmt_check_booking = text("""
                SELECT 1 FROM students_booking 
                WHERE student_id = :student_id AND time_slot_id = :time_slot_id
                LIMIT 1
            """)
            booking = db.execute(stmt_check_booking, {
                "student_id": user_id,
                "time_slot_id": r["id"]
            }).fetchone()

            if booking:
                # 已经预约 → 黄色
                color = "#fff3cd"        # 背景黄色
                border_color = "#ffecb5" # 边框浅黄
                text_color = "#664d03"   # 深黄色字体   
                canBook = False

        events.append({
            "id": r["id"],
            "title": r["title"],
            "start": r["start"],
            "end": r["end"],
            "status": r["status"],
            "color": color,
            "borderColor": border_color,
            "textColor": text_color,
            "canBook": canBook
        })
    return events