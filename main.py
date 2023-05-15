from fastapi import Depends, FastAPI, Request
from App.core.auth.middlewares.AuthorizationMiddleware import token_middleware
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles

from App.input_ports.routes.api import order_routes
from App.input_ports.routes.system.settings import Payment_route
from App.input_ports.routes.system import user_routes
from App.input_ports.routes.api import product_routes

from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI(title="TOOLBROTHER API", version="1.0.0", description="This API is to design the Toolbrother dashboard",docs_url="/toolbrothers_api/docs") 

@app.get('/', tags=["Welcome"], include_in_schema=False)
def welcome(): return {"Message": "Welcome one api on", "Version": "1.0.0", "Build by": "TOOLBROTHER Enterprise"}

origins = [
    "http://localhost:5173" 
]

app.include_router(order_routes.api_route)
app.include_router(user_routes.s_user_route)
app.include_router(product_routes.api_route)
app.include_router(Payment_route.route)
 
# static files
# app.mount("/static", StaticFiles(directory="static"), name="static")

# cors
app.add_middleware( 
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
# authorizations
# app.add_middleware(BaseHTTPMiddleware, dispatch=orders_permissions)

# app.add_middleware(BaseHTTPMiddleware, dispatch=firewall_middleware)
# app.add_middleware(BaseHTTPMiddleware, dispatch=token_middleware)

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=6540)