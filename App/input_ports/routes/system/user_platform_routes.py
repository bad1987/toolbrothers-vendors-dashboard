from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request, status
from App.Http.Schema.PlatformSchema import PlatformTypeSchema, PlatformSchemaOut, PlatformFieldValuesSchema, PlatformUserSchema, UserPlatformSchema
from App.core.auth.Acls.RoleChecker import Role_checker
from App.core.auth.auth import is_authenticated
from App.core.dependencies.db_dependencies import get_db
from App.output_ports.models.Models import Platform, User, User_Platform
from sqlalchemy.orm import Session
import json

from rich.console import Console as console

roles_checker = Role_checker()

route = APIRouter(prefix='/users', tags=['Users Platforms'], include_in_schema=False)

@route.get("/platform")
def get_platform_list(request: Request, db: Session = Depends(get_db), _user: dict = Depends(is_authenticated)):
    platform = _user.platform

    if platform is None or platform.status is False:
        raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not able to access this product"
            )

    vals = db.query(User_Platform).filter(User_Platform.user_id == _user.id).first()

    fields = []
    values = []

    for key, value in json.loads(platform.fields).items():
        fields.append(PlatformTypeSchema(
            name=key,
            type=value
        ))

    if vals is not None:
        for key, value in json.loads(vals.values).items():
            values.append(PlatformFieldValuesSchema(
                name=key,
                value=value
            ))

    return UserPlatformSchema(
        id=platform.id,
        name=platform.name,
        fields=fields,
        status=platform.status,
        values=values
    )

@route.put("/platform")
def update_platform(request: Request, model: UserPlatformSchema, db: Session = Depends(get_db), _user: dict = Depends(is_authenticated)):
    platform = _user.platform
    vals = db.query(User_Platform).filter(User_Platform.user_id == _user.id).first()

    if vals is None:
        vals = User_Platform(
            user_id=_user.id,
            platform_id=platform.id,
            values=json.dumps({})
        )
        db.add(vals)
        db.commit()
        db.refresh(vals)

    values = {}

    for val in model.values:
        values[val.name] = val.value

    vals.values = json.dumps(values)

    db.commit()
    db.refresh(vals)

    return model