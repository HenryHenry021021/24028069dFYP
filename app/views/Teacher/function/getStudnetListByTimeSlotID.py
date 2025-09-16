from fastapi import APIRouter, Depends, Request
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.DBconnection import get_db 

router = APIRouter()

@router.get("/getStudentListByTimeSlotID")
async def get_student_list_by_time_slot_id(
    time_slot_id: int,
    request: Request,
    database: Session = Depends(get_db)
):
    # 1️⃣ 查 slot info
    stmt_slot = text("""
        SELECT id, title, timeSlotGroupId, start, end, status, teacher_id, content, capacity
        FROM booking_time_slot
        WHERE id = :time_slot_id
    """)
    slot = database.execute(stmt_slot, {"time_slot_id": time_slot_id}).mappings().first()

    if not slot:
        return {"error": "Time slot not found"}

    # 2️⃣ 查學生 (Matched 狀態) → 不用縮寫，全部全稱
    stmt_students = text("""
        SELECT 
            students_booking.booking_id,
            students_booking.student_id,
            users.full_name AS student_name,
            users.email,
            users.year_of_study,
            students_booking.priority,
            students_booking.status
        FROM students_booking
        INNER JOIN users 
            ON students_booking.student_id = users.id
        WHERE students_booking.time_slot_id = :time_slot_id
        AND students_booking.status = 'Matched'
        ORDER BY students_booking.priority ASC
    """)

    result = database.execute(stmt_students, {"time_slot_id": time_slot_id}).mappings().all()

    students = []
    for r in result:
        student = {
            "booking_id": r["booking_id"],
            "student_id": r["student_id"],
            "student_name": r["student_name"],
            "email": r["email"],
            "year_of_study": r["year_of_study"],
            "priority": r["priority"],
            "status": r["status"]
        }
        students.append(student)

    # 3️⃣ return 結果
    return [
        {
            "slot": {
                "id": slot["id"],
                "title": slot["title"],
                "timeSlotGroupId": slot["timeSlotGroupId"],
                "start": str(slot["start"]),
                "end": str(slot["end"]),
                "status": slot["status"],
                "teacher_id": slot["teacher_id"],
                "content": slot["content"],
                "capacity": slot["capacity"]
            }
        },
        {
            "students": students
        }
    ]
