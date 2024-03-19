""" common menu GNB """
from datetime import datetime


from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse,JSONResponse


from app.utils import Template, log


router = APIRouter()
log.info(__name__)

@router.get("/sidebar", response_class=HTMLResponse)
async def main_sidebar(request: Request) -> HTMLResponse:
    """gnb"""
    return Template().TemplateResponse(
        "common/menu/main_sidebar.html",
        context={'request': request, "datetime": "value"}
    )