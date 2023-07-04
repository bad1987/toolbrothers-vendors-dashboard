from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request, status
from App.Http.Schema.PlatformSchema import PlatformTypeSchema, PlatformSchemaOut, PlatformFieldValuesSchema, PlatformUserSchema, UserPlatformSchema
from App.core.auth.Acls.RoleChecker import Role_checker
from App.core.auth.auth import is_authenticated
from App.core.dependencies.db_dependencies import get_db
from App.output_ports.models.Models import Platform, Platform_Data, User, User_Platform
from sqlalchemy.orm import Session
import json

from rich.console import Console as console

roles_checker = Role_checker()

route = APIRouter(prefix='/users', tags=['Users Platforms'], include_in_schema=False)

@route.get("/platform")
def get_platform_list(request: Request, db: Session = Depends(get_db), _user: dict = Depends(is_authenticated)):
    platform = _user.platform
    platform_data = db.query(Platform_Data).filter(Platform_Data.platform_id == platform.id).filter(Platform_Data.language == _user.default_language.value).first()

    if platform is None or platform_data is None or platform.status is False:
        raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not able to access this section"
            )

    vals = db.query(User_Platform).filter(User_Platform.user_id == _user.id).first()

    fields = []
    values = []
    name_list = []

    for key, value in json.loads(platform_data.fields).items():
        fields.append(PlatformTypeSchema(
            name=key,
            type=value
        ))
        name_list.append(key)

    

    if vals is not None:
        for key, value in json.loads(vals.values).items():
            values.append(PlatformFieldValuesSchema(
                name=name_list[int(key)],
                value=value,
            ))

    return UserPlatformSchema(
        id=platform.id,
        name=platform_data.name,
        fields=fields,
        status=platform.status,
        values=values
    )

@route.put("/platform")
def update_platform(request: Request, model: UserPlatformSchema, db: Session = Depends(get_db), _user: dict = Depends(is_authenticated)):
    platform = _user.platform
    user_platform = db.query(User_Platform).filter(User_Platform.user_id == _user.id).first()
    datas = db.query(Platform_Data).filter(Platform_Data.platform_id == platform.id).first()

    values = {}
    model_values = model.values

    for index, key in enumerate(json.loads(datas.fields)):
        values[index] = model_values[index].value

    if user_platform == None:
        db.add(User_Platform(
            values = json.dumps(values),
            user_id = _user.id,
            platform_id = platform.id,
        ))
    else:
        user_platform.values = json.dumps(values)
    

    db.commit()

    return model