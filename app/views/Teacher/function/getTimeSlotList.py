from fastapi import APIRouter, Depends, Request
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.DBconnection import get_db 

router = APIRouter()

@router.get("/getTimeSlotList")
async def get_time_slot_list(request: Request, db: Session = Depends(get_db)):
    teacher_id = request.cookies.get("user_id")
    if not teacher_id:
        return []

    stmt = text("""
        SELECT id, title, timeSlotGroupId, start, end, status, teacher_id, content, capacity
        FROM booking_time_slot
        WHERE teacher_id = :teacher_id
        ORDER BY start DESC
    """)
    result = db.execute(stmt, {"teacher_id": teacher_id}).mappings().all()

    groups = {}
    for r in result:
        gid = r["timeSlotGroupId"]
        if gid not in groups:
            groups[gid] = {
                "timeSlotGroupId": gid,
                "slots": []
            }
        slot = {
            "id": r["id"],
            "title": r["title"],
            "start": str(r["start"]),
            "end": str(r["end"]),
            "status": r["status"],
            "teacher_id": r["teacher_id"],
            "content": r["content"],
            "capacity": r["capacity"],
            "date": str(r["start"]).split(" ")[0] if r["start"] else None
        }
        groups[gid]["slots"].append(slot)

    return list(groups.values())
