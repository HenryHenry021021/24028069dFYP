# app/clearCookies.py
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/clearCookies")
async def clear_cookies(request: Request):
    response = JSONResponse({"message": "All cookies cleared"})
    for cookie_name in request.cookies.keys():
        response.delete_cookie(cookie_name)
    return response
