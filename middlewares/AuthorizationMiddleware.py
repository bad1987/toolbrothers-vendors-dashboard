from fastapi import HTTPException, Request, status
from fastapi.responses import RedirectResponse
from Database.Models import Login_Attempt

from Security.Acls.RoleChecker import Role_checker
from Database.Connexion import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def orders_permissions(request: Request, call_next):
    permission = Role_checker(['Role_affiliate', 'Role_direct_sale', 'Role_admin'])
    # check if the user has the permissions
    if request.url.path.startswith("/orders"):
        db = SessionLocal()
        try:
            permission(request, db)
            db.close()
        except HTTPException as e:
            print(str(e.detail), e.status_code)
            db.close()
            return RedirectResponse("/errors/403")
        
    response = await call_next(request)
    return response

async def block_ip_middleware(request: Request, call_next):
    # Récupération de l'adresse IP du client
    ip_address = request.client.host

    # Vérification si l'adresse IP est bloquée
    session = SessionLocal()
    attempt = session.query(Login_Attempt).filter(
        Login_Attempt.ip == ip_address
    ).first()
    if attempt != None and attempt.count >= 3:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Your ip is blocked")

    # Si l'adresse IP n'est pas bloquée, on continue le traitement de la requête
    response = await call_next(request)
    
    return response