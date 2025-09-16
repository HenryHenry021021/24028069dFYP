from fastapi import APIRouter, Depends, Request
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.DBconnection import get_db 
router = APIRouter()

@router.get("/getTimeSlotForTeacher")
async def get_events(teacher_id: int, request: Request, db: Session = Depends(get_db)):
    # 这就是 prepared statement
    user_id = request.cookies.get("user_id")

    stmt = text("""
        SELECT id, title, start, end, status
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