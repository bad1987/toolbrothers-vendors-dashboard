import time
from fastapi import HTTPException, Request, APIRouter, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


route = APIRouter(prefix='/errors', tags=['Handle Errors response'], include_in_schema=False)
templates = Jinja2Templates(directory="templates")

@route.get("/403", response_class=HTMLResponse)
async def error_403(request: Request):
    context = {
        'request': request
    }

    return templates.TemplateResponse("errors/403.html", context)


@route.get("/401")
async def error_401(request: Request):
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated"
    )
