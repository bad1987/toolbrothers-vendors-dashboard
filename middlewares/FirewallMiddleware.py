from fastapi import Request
from fastapi.responses import RedirectResponse
from Security.Controllers.LoginController import is_authenticated

async def firewall_middleware(request: Request, call_next):
    allowed_routes = ['/auth/login', '/docs', '/favicon.ico', '/auth/logout']
    url = request.url.path
    if not url in allowed_routes and url.startswith("/errors"):
        allowed_routes.append(url)
    cookie = request.headers.get('Cookie')
    # print(request.headers.get('Cookie'))
    if request.url.path not in allowed_routes:
        # cookie deleted
        if not cookie:
            return RedirectResponse("/errors/401", status_code=401)
        # cookie expired
        user = is_authenticated(request)
        if not user:
            return RedirectResponse("/auth/login")
    response = await call_next(request)
    return response

async def orders_permissions(request: Request, call_next):
    allowed_roles = ['Role_affiliate', 'Role_direct_sale', 'Role_admin']