import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from fastapi import Response

# ========= 数据库配置 =========
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def check_login_service(email: str, password: str, captcha: str, captcha_email: str, captcha_code: str,  response: Response):
    """校验登录逻辑"""
    # 1) 检查验证码
    if captcha_email != email:
        return {"error": "❌ Email not match captcha"}
    if captcha_code != captcha:
        return {"error": "❌ Wrong captcha"}

    # 2) 连接数据库
    db = SessionLocal()
    try:
        stmt = text("SELECT * FROM users WHERE email=:email LIMIT 1")
        result = db.execute(stmt, {"email": email}).fetchone()
        if not result:
            return {"error": "❌ No such user"}

        user = dict(result._mapping)
        if user["password"] != password:
            return {"error": "❌ Incorrect password"}

        # 3) 登录成功
        response.set_cookie(
            key="user_id",
            value=str(user["id"]),
            max_age=3600,     # 1 小时有效
            path="/"
        )

        response.set_cookie(
            key="role",
            value=str(user["role_id"]),   # 直接存數字
            max_age=3600,
            path="/"
        )
        role = str(user["role_id"])
        if role == "2":
            return {"status": "OK", "redirect": "/static/views/Teacher/createTimeSlot.html"}
        elif role == "1":
            return {"status": "OK", "redirect": "/static/views/Student/studentViewBookingGroup.html"}
        else:
            return {"status": "OK", "redirect": "dashboard.php"}
    except Exception as e:
        return {"error": f"❌ DB error: {str(e)}"}
    finally:
        db.close()
