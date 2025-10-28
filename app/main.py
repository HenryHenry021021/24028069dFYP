from fastapi import FastAPI, Response, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from app.send_captcha import generate_code, send_captcha_email
from app.check_login_data import check_login_service
from fastapi import FastAPI, Form, Request, Response
from app.views.Student.function.getTimeSlot import router as timeslot_router
from app.views.Student.function.getTeachersNameList import router as getTeachersNameList_router
from app.views.Student.function.reserveTimeSlot import router as reserveTimeSlot_router
from app.views.Student.function.myUpcomingBookings import router as myUpcomingBookings_router
from app.views.Student.function.getTimeslotGroup import router as getTimeslotGroup_router
from app.views.Student.function.cancelBooking import router as cancelBooking_router
from fastapi import WebSocket
from app.websocket_manager import connect_client, disconnect_client
from app.clearCookies import router as clearCookies_router


from app.views.Teacher.function.getTimeSlotForTeacher import router as getTimeSlotForTeacher_router
from app.views.Teacher.function.createTimeSlot import router as createTimeSlot_router
from app.views.Teacher.function.getTimeSlotList import router as getTimeSlotList_router
from app.views.Teacher.function.getStudnetListByTimeSlotID import router as getStudnetListByTimeSlotID_router
from app.views.Teacher.function.matchAlgorithm import router as matchAlgorithm_router


# ========= 初始化 FastAPI =========
app = FastAPI()
app.include_router(timeslot_router, prefix="/api")
app.include_router(getTeachersNameList_router, prefix="/api")
app.include_router(myUpcomingBookings_router, prefix="/api")
app.include_router(getTimeslotGroup_router, prefix="/api")
app.include_router(cancelBooking_router, prefix="/api")
app.include_router(clearCookies_router, prefix="/api")



app.include_router(reserveTimeSlot_router, prefix="/api")
app.include_router(getTimeSlotForTeacher_router, prefix="/api")
app.include_router(createTimeSlot_router, prefix="/api")
app.include_router(getTimeSlotList_router, prefix="/api")
app.include_router(getStudnetListByTimeSlotID_router, prefix="/api")
app.include_router(matchAlgorithm_router, prefix="/api")


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 可以改成前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="app/"), name="static")
# 模板 & 静态资源
templates = Jinja2Templates(directory="app/views")


# ========= 首页 =========
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# ========= 发送验证码 =========
@app.get("/api/send-captcha")
async def send_captcha(email: str, response: Response):
    code = generate_code()
    try:
        send_captcha_email(email, code)

        # 存 cookie
        response.set_cookie(key="captcha_code", value=code, max_age=300, path="/")
        response.set_cookie(key="captcha_email", value=email, max_age=300, path="/")

        return {"status": "✅ Captcha sent", "email": email}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/api/check-login")
async def check_login(
    response: Response,

    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    captcha: str = Form(...)
):
    # 从 cookie 获取验证码信息
    captcha_email = request.cookies.get("captcha_email")
    captcha_code = request.cookies.get("captcha_code")

    # 调用外部方法
    result = check_login_service(email, password, captcha, captcha_email, captcha_code, response)

    
    if "error" in result:
     return JSONResponse(content=result, status_code=200)  # ⬅️ 这里是 400
    return result

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await connect_client(ws)
    try:
        while True:
            data = await ws.receive_text()
            print("收到:", data)
    except:
        await disconnect_client(ws)
