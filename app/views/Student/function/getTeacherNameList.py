from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.DBconnection import get_db

router = APIRouter()

@router.get("/getTeachersNameList")
async def get_teachers(db: Session = Depends(get_db)):
    sql = text("SELECT id, full_name FROM users WHERE role_id = 2 ORDER BY full_name ASC")
    rows = db.execute(sql).mappings().all()

    teachers = []
    for r in rows:
        teachers.append({
            "id": int(r["id"]),
            "name": r["full_name"]
        })
    return teachers
