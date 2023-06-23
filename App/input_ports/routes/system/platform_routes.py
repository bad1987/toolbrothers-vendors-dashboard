from typing import List
from fastapi import APIRouter, Depends, Request
from App.Http.Schema.PlatformSchema import PlatformTypeSchema, PlatformSchemaOut, PlatformFieldValuesSchema, PlatformUserSchema
from App.core.auth.Acls.RoleChecker import Role_checker
from App.core.auth.auth import is_authenticated
from App.core.dependencies.db_dependencies import get_db
from App.output_ports.models.Models import Platform, User
from sqlalchemy.orm import Session
import json


roles_checker = Role_checker()

route = APIRouter(prefix='/admin', tags=['Platforms system'], include_in_schema=False)

@route.get("/platforms", response_model=List[PlatformSchemaOut])
def get_platform_list(request: Request, db: Session = Depends(get_db), _user: dict = Depends(is_authenticated)):
    platforms = db.query(Platform).all()

    result = []

    for platform in platforms:
        fields = json.loads(platform.fields)
        ans = []

        for key, value in fields.items():
            ans.append(PlatformTypeSchema(**{'name': key, 'type': value}))

        result.append(PlatformSchemaOut(**{'id': platform.id, 'name': platform.name, 'fields': ans, 'status': platform.status}))

    return result

@route.post("/platforms", response_model=PlatformSchemaOut)
def create_platform(request: Request, model: PlatformSchemaOut, db: Session = Depends(get_db), _user: dict = Depends(is_authenticated)):
    fields = {}
    for field in model.fields:
        key, value = field.name, field.type
        fields[key] = value.value

    platform = Platform(name=model.name, fields=json.dumps(fields), status=model.status)
    db.add(platform)
    db.commit()
    db.refresh(platform)

    return model

@route.put("/platforms/{id}", response_model=PlatformSchemaOut)
def update_platform(id: int, request: Request, model: PlatformSchemaOut, db: Session = Depends(get_db), _user: dict = Depends(is_authenticated)):
    platform = db.query(Platform).filter(Platform.id == id).first()
    fields = {}
    for field in model.fields:
        key, value = field.name, field.type
        fields[key] = value.value

    platform.name = model.name
    platform.fields = json.dumps(fields)
    platform.status = model.status

    db.commit()
    db.refresh(platform)

    return model

@route.delete("/platforms/{id}")
def delete_platform(id: int, request: Request, db: Session = Depends(get_db), _user: dict = Depends(is_authenticated)):
    platform = db.query(Platform).filter(Platform.id == id).first()
    db.delete(platform)
    db.commit()

    return {}
