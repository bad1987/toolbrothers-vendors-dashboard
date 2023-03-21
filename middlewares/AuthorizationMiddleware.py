from fastapi import HTTPException, Request
from fastapi.responses import RedirectResponse

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