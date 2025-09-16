from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.DBconnection import get_db 

router = APIRouter()

# 请求体模型
class ReserveRequest(BaseModel):
    time_slot_id: int


@router.post("/reserveTimeSlot")
async def reserve_time_slot(payload: ReserveRequest, request:Request, db: Session = Depends(get_db)):
    student_id = request.cookies.get("user_id")  # 从 cookie 取登录用户 id 
    if not student_id:
        raise HTTPException(status_code=401, detail="Not logged in")

    # 取出参数
    time_slot_id = payload.time_slot_id

    # 查詢 timeslot 狀態
    stmt_check = text("""
        SELECT *
        FROM booking_time_slot 
        WHERE id = :time_slot_id
    """)
    slot = db.execute(stmt_check, {"time_slot_id": time_slot_id}).mappings().first()

    groupID= slot['timeSlotGroupId']

    if not slot:
        raise HTTPException(status_code=404, detail="Time slot not found")

    if slot["status"] != "Available":
        raise HTTPException(status_code=400, detail="Time slot not available")

    # 1️⃣ 查詢學生的 year_of_study
    stmt_year = text("""
        SELECT year_of_study 
        FROM users 
        WHERE id = :student_id
    """)
    student = db.execute(stmt_year, {"student_id": student_id}).mappings().first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    priority_value = student["year_of_study"]  # 用 year 當 priority

    # 查這個 group 一共有多少 slot
    stmt_group_slot_count = text("""
        SELECT COUNT(*) AS group_slot_count
        FROM booking_time_slot
        WHERE timeSlotGroupId = :gid
    """)
    slot_count_result = db.execute(stmt_group_slot_count, {"gid": groupID}).mappings().first()
    group_slot_count = slot_count_result["group_slot_count"] if slot_count_result else 0



    stmt_student_group_count = text("""
        SELECT COUNT(*) AS booked_count
        FROM students_booking sb
        INNER JOIN booking_time_slot ts ON sb.time_slot_id = ts.id
        WHERE sb.student_id = :student_id
        AND ts.timeSlotGroupId = :gid
    """)
    result = db.execute(stmt_student_group_count, {
        "student_id": student_id,
        "gid": groupID
    }).mappings().first()

    student_booked_count = result["booked_count"] if result else 0

        
    
    priority_value = priority_value + (group_slot_count-student_booked_count)

    # 2️⃣ 插入预约，帶上 priority
    stmt_insert = text("""
        INSERT INTO students_booking (student_id, time_slot_id, priority)
        VALUES (:student_id, :time_slot_id, :priority)
    """)
    db.execute(stmt_insert, {
        "student_id": student_id, 
        "time_slot_id": time_slot_id, 
        "priority": priority_value
    })
    db.commit()

    

    return {
    "status": "ok",
    "msg": f"Student {student_id} reserved time slot {time_slot_id}",
    "priority": priority_value,
    "slot_count_under_group": group_slot_count,
    "student_booked_count": student_booked_count,
    "groupID": groupID
}

