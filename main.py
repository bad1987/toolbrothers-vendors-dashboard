from fastapi import FastAPI
from passlib.handlers.sha2_crypt import sha512_crypt as crypto
from Database import Models
from Database.Connexion import engine
import uvicorn
from Security.Routes.Login_register import Login_register

Models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(Login_register.route) 

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=9000)