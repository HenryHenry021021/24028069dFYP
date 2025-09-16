from fastapi import APIRouter, Depends, Form
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.DBconnection import get_db
from typing import List
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

router = APIRouter()

SMTP_HOST = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("EMAIL_USER")
SMTP_PASS = os.getenv("EMAIL_PASS")
SMTP_FROM = os.getenv("SMTP_FROM", SMTP_USER)
SMTP_FROM_NAME = os.getenv("SMTP_FROM_NAME", "FastAPI Service")

@router.post("/mactchAlgorithm")
async def get_booked_students_in_group(
    time_slot_id: int = Form(...),   # ✅ 改這裡，讓 FastAPI 從 form-data 解析
    db: Session = Depends(get_db)
):
    # 查這個 slot 的 groupId
    stmt_group = text("SELECT timeSlotGroupId, capacity FROM booking_time_slot WHERE id = :time_slot_id")
    group_row = db.execute(stmt_group, {"time_slot_id": time_slot_id}).mappings().first()

    if not group_row:
        return {"error": "time slot not found"}

    group_id = group_row["timeSlotGroupId"]
    capacity = group_row["capacity"]

    # 查同 group 其他 slot (只取 id)
    stmt_slots = text("""
        SELECT id
        FROM booking_time_slot
        WHERE timeSlotGroupId = :group_id
          AND id != :time_slot_id
    """)
    rows = db.execute(stmt_slots, {
        "group_id": group_id,
        "time_slot_id": time_slot_id
    }).mappings().all()

    # 遍歷 rows，放進 list
    other_ids = []
    for r in rows:
        other_ids.append(r["id"])

    
    stmt_student = text("""
        SELECT student_id
        FROM students_booking
        WHERE time_slot_id = :time_slot_id
          AND status = 'Booked'
        ORDER BY priority DESC, created_at ASC
    """)
    rows_student = db.execute(stmt_student, {"time_slot_id": time_slot_id}).mappings().all()

    students_json = []
    for row_student in rows_student:  # 普通 for loop
        students_json.append({"student_id": row_student["student_id"]})

    updated_students = []
    numberMatchedStudent = 0
    for student in students_json:
        if numberMatchedStudent >= capacity:
            break

        match_in_other_slot = False
        for other_id in other_ids:
            stmt_check = text("""
                SELECT * 
                FROM students_booking
                WHERE student_id = :student_id
                AND time_slot_id = :other_id
                AND (status != 'Booked' AND status != 'Cancel')
            """)
            rows_check = db.execute(stmt_check, {
                "student_id": student["student_id"],
                "other_id": other_id
            }).mappings().all()

            if rows_check:  # 有紀錄 → 說明學生在其他 slot 已經不是 Booked
                match_in_other_slot = True
                break

            if not match_in_other_slot:
                stmt_update = text("""
                    UPDATE students_booking
                    SET status = 'Matched'
                    WHERE time_slot_id = :time_slot_id
                    AND student_id = :student_id
                """)
                db.execute(stmt_update, {
                    "time_slot_id":time_slot_id,   # 單筆 booking_id
                    "student_id": student["student_id"]    # 對應的學生
                })
                numberMatchedStudent += 1
                updated_students.append(student["student_id"])
                break

    stmt = text("""
        UPDATE booking_time_slot
        SET status = 'Reserved'
        WHERE id = :time_slot_id
    """)
    db.execute(stmt, {"time_slot_id": time_slot_id})
    db.commit()





    #  回傳結果
    return {
        "time_slot_id": time_slot_id,
        "group_id": group_id,
        "capacity": capacity,
        "other_slot_ids": other_ids,
        "student_list_in_this_slot": students_json,
        "number_matched": numberMatchedStudent,
        "updated_students": updated_students  
    }

@router.post("/notifyMatchedStudents")
async def notify_matched_students(time_slot_id: int, updated_students: list):

    return {"msg": "Notified", "time_slot_id": time_slot_id, "students": updated_students}
