from fastapi import Request
from fastapi.responses import RedirectResponse
from Security.Controllers.LoginController import is_authenticated

async def firewall_middleware(request: Request, call_next):
    allowed_routes = ['/auth/login', '/docs', '/favicon.ico', '/auth/logout']
    cookie = request.headers.get('Cookie')
    if request.url.path not in allowed_routes:
        # cookie deleted
        if not cookie:
            return RedirectResponse("/auth/login")
        # cookie expired
        user = is_authenticated(request)
        if not user:
            return RedirectResponse("/auth/login")
    response = await call_next(request)
    return response