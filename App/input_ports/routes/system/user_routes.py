from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from App.core.auth.middlewares.AuthorizationMiddleware import TokenMiddleware
from App.core.dependencies.db_dependencies import get_db
from App.core.use_cases.user_use_case import UserUsecase
from App.input_ports.schemas.UserSchema import UserListSchema, UserSchema


s_user_route = APIRouter(prefix='/admin', tags=['Users system'], include_in_schema=False)

@s_user_route.get("/users/{type}/list")
# @requires_permission('read', ModelNameEnum.USER_MODEL.value)
async def get_users_list(
    request: Request,
    type: str,
    db: Session = Depends(get_db)
):
    user_usecase = UserUsecase(db)
    users = user_usecase.get_users_by_type(request, type)
    permissions = user_usecase.get_permissions()
    return {
        "users": users,
        "permissions": permissions,
    }

@s_user_route.get("/user", response_model= UserSchema | None)
def get_user(request: Request, db: Session = Depends(get_db)):
    print('getting the user')
    user_usecase = UserUsecase(db)
    user = user_usecase.get_user(request=request)
    return user