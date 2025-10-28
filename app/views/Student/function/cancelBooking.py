from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.DBconnection import get_db

router = APIRouter()

@router.post("/cancelBooking")
async def cancel_booking(payload: dict, request: Request, db: Session = Depends(get_db)):
    student_id = request.cookies.get("user_id")
    booking_id = payload.get("booking_id")

   


    try:
        # 1️⃣ 找到 slot_id（確保這筆 booking 屬於這個學生）
        stmt_find = text("""
            SELECT time_slot_id
            FROM students_booking
            WHERE booking_id = :bid AND student_id = :sid
        """)
        row = db.execute(stmt_find, {"bid": booking_id, "sid": student_id}).fetchone()

        if not row:
            return {"error": "找不到 booking 或不是你的紀錄"}

        slot_id = row[0]

        # 2️⃣ 先刪除 booking
        stmt_delete = text("""
            DELETE FROM students_booking
            WHERE booking_id = :bid AND student_id = :sid
        """)
        delete_result = db.execute(stmt_delete, {"bid": booking_id, "sid": student_id})

        if delete_result.rowcount == 0:
            db.rollback()
            return {"error": "刪除失敗，可能已被刪除"}

        # 3️⃣ 鎖定 slot
        stmt_lock = text("""
            SELECT vacancy
            FROM booking_time_slot
            WHERE id = :slot_id
            FOR UPDATE
        """)
        lock_row = db.execute(stmt_lock, {"slot_id": slot_id}).fetchone()

        if not lock_row:
            db.rollback()
            return {"error": "找不到 slot"}

        # 4️⃣ vacancy + 1
        stmt_update = text("""
            UPDATE booking_time_slot
            SET vacancy = vacancy + 1
            WHERE id = :slot_id
        """)
        update_result = db.execute(stmt_update, {"slot_id": slot_id})

        db.commit()
        return {"success": True, "booking_id": booking_id, "slot_id": slot_id}

    except Exception as e:
        db.rollback()
        print("[ERROR] cancel_booking 失敗:", str(e))
        return {"error": str(e)}
