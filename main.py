from fastapi import FastAPI
from Database import Models
from Database.Connexion import engine
import uvicorn
from Security.Routes.Login_register import Login_register
from Routes import Users, Orders, Errors, Payments

from middlewares.FirewallMiddleware import firewall_middleware
from middlewares.AuthorizationMiddleware import orders_permissions
from starlette.middleware.base import BaseHTTPMiddleware

from fastapi.staticfiles import StaticFiles

# Models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(Login_register.route) 
app.include_router(Users.route) 
app.include_router(Orders.route)
app.include_router(Errors.route)
app.include_router(Payments.route)

# static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# authorizations
app.add_middleware(BaseHTTPMiddleware, dispatch=orders_permissions)
# allow only authenticated users
app.add_middleware(BaseHTTPMiddleware, dispatch=firewall_middleware)

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=9000)