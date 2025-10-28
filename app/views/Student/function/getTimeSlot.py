from fastapi import APIRouter, Depends, Request
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.DBconnection import get_db 
router = APIRouter()
import os

@router.get("/getTimeSlot")
async def get_events(group_id: str, db: Session = Depends(get_db)):
    stmt = text("""
        SELECT 
            id,
            title,
            start,
            end,
            content,
            vacancy,
            deadline
        FROM booking_time_slot
        WHERE timeSlotGroupId = :group_id
        ORDER BY start ASC
    """)

    result = db.execute(stmt, {"group_id": group_id}).mappings().all()
    return result

@router.get("/configWebSocket")
async def get_config():
    return {
        "WS_HOST": os.getenv("WS_HOST", "localhost:8000"),
        "WS_PATH": os.getenv("WS_PATH", "/ws"),
    }
