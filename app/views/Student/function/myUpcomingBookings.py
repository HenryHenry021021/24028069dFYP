from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import text
from sqlalchemy.orm import Session
from datetime import date
from app.DBconnection import get_db 

router = APIRouter()

@router.get("/myUpcomingBookings")
async def get_my_upcoming_bookings(request: Request, db: Session = Depends(get_db)):
    """
    查詢今天 & 未來的 booking（JOIN booking_time_slot, users）
    """
    student_id = request.cookies.get("user_id")
    if not student_id:
        raise HTTPException(status_code=401, detail="Not logged in")

    today_str = date.today().strftime("%Y-%m-%d")

    stmt = text("""
        SELECT 
            sb.booking_id,
            sb.student_id,
            sb.time_slot_id,
            sb.status AS booking_status,
            sb.created_at,
            ts.start,
            ts.end,
            ts.title,
            ts.content,
            ts.capacity,
            ts.status AS slot_status,
            u.full_name AS teacher_name,
            u.email AS teacher_email
        FROM students_booking sb
        JOIN booking_time_slot ts ON sb.time_slot_id = ts.id
        JOIN users u ON ts.teacher_id = u.id
        WHERE sb.student_id = :student_id
        AND DATE(ts.start) >= :today
        AND sb.status = 'Booked'
        ORDER BY ts.start ASC
    """)
    results = db.execute(
        stmt, {"student_id": student_id, "today": today_str}
    ).mappings().all()

    return {
        "status": "ok",
        "today_or_future": results
    }
