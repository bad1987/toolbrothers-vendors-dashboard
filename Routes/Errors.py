import time
from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


route = APIRouter(prefix='/errors')
templates = Jinja2Templates(directory="templates")

@route.get("/403", response_class=HTMLResponse)
async def error_403(request: Request):
    context = {
        'request': request
    }

    return templates.TemplateResponse("errors/403.html", context)
