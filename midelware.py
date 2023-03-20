from fastapi import FastAPI, Request, Response, status, WebSocket, WebSocketException, Query
import requests
import uvicorn
from starlette.middleware.cors import CORSMiddleware
import sys
import config
from src.Database.connexion import engine
from functools import lru_cache
from fastapi.responses import JSONResponse
from src.Database import models
from src.Routes import apiRoutes

models.Base.metadata.create_all(engine)

app = FastAPI()

@app.exception_handler(Exception)
async def events_app_handler(request: Request, call_next):
    try: return await call_next(request)
    except Exception: return Response("Internal server error", status_code=500)

@app.get('/', tags=["Welcome"])
def welcome(): return {"Message": "Welcome On API Messenger", "Version": "1.0.0", "Build by": "Klapeers Enterprise"}

@app.get('/health', tags=["Health"])
def health(): return {"status": "UP"}

app.include_router(apiRoutes.router) 
app.include_router(apiRoutes.participant)
app.include_router(apiRoutes.groupConversations)
app.include_router(apiRoutes.singleConversations) 
 
ALLOWED_ORIGINS = '*' 
@app.middleware("http")
async def add_CORS_header(request: Request, call_next):
    # If request method ins OPTIONS server responde with response headers
    if request.method == 'OPTIONS':
        response = Response()
        response.headers['Access-Control-Allow-Origin'] = ALLOWED_ORIGINS
        response.headers['Access-Control-Allow-Methods'] = 'POST, GET, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type'
        return response
    
    # Get free access for docs api and public routes 
    public_routes = [
        '/',
        '/docs',
        '/health',
        '/favicon.ico',
        '/openapi.json',
    ]
    if request.url.path in public_routes:
        response = await call_next(request)
        return response

    #  Check bearer token in header request
    token = request.headers.get('Authorization')
    try:
        # Check valaidity of token
        url = config.AUTH_SERVER_BASE_URL+"/users/me"
        headers = {
            'Authorization': token
        }
        response_verification = requests.request("GET", url, headers=headers)

        if int(response_verification.status_code) != 200:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={
                "response": {
                    "status": "error",
                    "code": 401,
                    "message": "Token is invalid or has expired",
                }
            })
            
        # Get users infos and set it in request
        request.state.user_attr = {"user_info": response_verification.json()}
        
        response = await call_next(request)
        response.headers['Access-Control-Allow-Origin'] = ALLOWED_ORIGINS
        response.headers['Access-Control-Allow-Methods'] = 'POST, GET, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type'

        return response
    except requests.HTTPError as e:
        raise JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={
            "response": {
                "status": "error",
                "code": 401,
                "message": "Unauthorized",
            }
        })

if __name__ == '__main__':
	uvicorn.run("main:app", host='0.0.0.0', port=int(sys.argv[1]), log_level="info", reload=True)  
   
