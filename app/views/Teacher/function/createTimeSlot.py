from typing import List
from fastapi import APIRouter, Depends, Form, Request
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.DBconnection import get_db 
import random, string

router = APIRouter()

@router.post("/createTimeSlot")
async def create_time_slot(
    request: Request,
    title: str = Form(...),
    start: List[str] = Form(...),   # 多個 start[]
    end: List[str] = Form(...),     # 多個 end[]
    status: str = Form("Available"),
    content: str = Form(None),
    capacity: int = Form(...),
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
                (title, timeSlotGroupId, start, end, status, teacher_id, content, capacity)
            VALUES 
                (:title, :gid, :start, :end, :status, :teacher_id, :content, :capacity)
        """)
        db.execute(insert_stmt, {
            "title": title,
            "gid": group_id,
            "start": start[i],
            "end": end[i],
            "status": status,
            "teacher_id": teacher_id,
            "content": content,
            "capacity": capacity
        })

    db.commit()
    return {"message": "All time slots created successfully", "timeSlotGroupId": group_id}
