from fastapi import FastAPI
from Database import Models
from Database.Connexion import engine
import uvicorn
from Security.Routes.Login_register import Login_register
from Routes import Users, Orders

Models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(Login_register.route) 
app.include_router(Users.route) 
app.include_router(Orders.route) 

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=9000)