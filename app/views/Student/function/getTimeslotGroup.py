from fastapi import APIRouter, Depends,Request
from sqlalchemy import text
from sqlalchemy.orm import Session
from datetime import datetime
from app.DBconnection import get_db

router = APIRouter()

@router.get("/getTimeslotGroup")
async def get_timslot_group(request: Request, db: Session = Depends(get_db)):
    # ⚠️ 暫時 hardcode user_id
    user_id = request.cookies.get("user_id")

    # 1️⃣ 找出學生參與的 group_id
    query_groups = text("""
        SELECT DISTINCT group_id
        FROM time_slot_group_student
        WHERE user_id = :uid
    """)
    group_rows = db.execute(query_groups, {"uid": user_id}).fetchall()
    group_ids = [row.group_id for row in group_rows]

    if not group_ids:
        return {"groups": []}

    today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    groups = []

    # 2️⃣ for loop 每個 group_id 單獨查
    for gid in group_ids:
        query_detail = text("""
            SELECT 
                booking_time_slot.id,
                booking_time_slot.timeSlotGroupId,
                booking_time_slot.title,
                users.full_name,
                booking_time_slot.content,
                booking_time_slot.deadline
            FROM booking_time_slot
            INNER JOIN users ON booking_time_slot.teacher_id = users.id
            WHERE booking_time_slot.timeSlotGroupId = :gid
              AND (booking_time_slot.deadline IS NULL OR booking_time_slot.deadline >= :today)
            LIMIT 1
        """)
        row = db.execute(query_detail, {"gid": gid, "today": today}).fetchone()

        if row:
        # 🔎 檢查學生是否已經在這個 slot 預約過
            query_slots = text("""
                SELECT id
                FROM booking_time_slot
                WHERE timeSlotGroupId = :gid
            """)
            slot_rows = db.execute(query_slots, {"gid": gid}).fetchall()
            slot_ids = [r[0] for r in slot_rows]

            if not slot_ids:
                continue  # 沒有 slot，跳過

            # 再查學生有沒有在這些 slot 裡已經 booking 過
            check_stmt = text("""
                SELECT 1
                FROM students_booking
                WHERE student_id = :sid
                AND time_slot_id IN :slot_ids
                LIMIT 1
            """)
            booked = db.execute(check_stmt, {"sid": user_id, "slot_ids": tuple(slot_ids)}).fetchone()

            if booked:
                continue  # 學生已經在這個 group 訂過了，跳過

            groups.append({
                "group_id": row.timeSlotGroupId,
                "title": row.title,
                "teacher_name": row.full_name,
                "content": row.content,
                "deadline": row.deadline
            })

    return {"groups": groups}