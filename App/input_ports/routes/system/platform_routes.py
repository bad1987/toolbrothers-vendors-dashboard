from typing import Dict, List
from fastapi import APIRouter, Depends, HTTPException, Request
from App.Http.Schema.PlatformSchema import AdminPlatformListSchema, AdminPlatformSchema, PlatformTypeSchema, PlatformSchemaOut, PlatformFieldValuesSchema, PlatformUserSchema
from App.core.auth.Acls.RoleChecker import Role_checker
from App.core.auth.auth import is_authenticated
from App.core.dependencies.db_dependencies import get_db
from App.output_ports.models.Models import Platform, Platform_Data, User, User_Platform
from sqlalchemy.orm import Session
import json


roles_checker = Role_checker()

route = APIRouter(prefix='/admin', tags=['Platforms system'], include_in_schema=False)

@route.get("/platforms", response_model=AdminPlatformListSchema)
def get_platform_list(request: Request, db: Session = Depends(get_db), _user: dict = Depends(is_authenticated)):
    platform_data = db.query(Platform_Data).all()

    result = []

    for data in platform_data:
        fields = []
        for key, value in json.loads(data.fields).items():
            fields.append(PlatformTypeSchema(name=key, type=value))

        result.append(AdminPlatformSchema(id=data.platform.id, name=data.name, fields=fields, status=data.platform.status, language=data.language))

    return AdminPlatformListSchema(platforms=result, languages=['de', 'en'])

@route.post("/platforms", response_model=Dict[str, str])
def create_platform(request: Request, model: List[AdminPlatformSchema], db: Session = Depends(get_db), _user: dict = Depends(is_authenticated)):
    
    try:
        platform = Platform(status=model[0].status)
        db.add(platform)


        for data in model:
            if data.name == None or data.name == '':
                raise HTTPException(status_code=422, detail="Name is required")

        db.commit()

        for data in model:
            fields = {}
            for field in data.fields:
                key, value = field.name, field.type
                fields[key] = value.value

            platform_data = Platform_Data(name=data.name, fields=json.dumps(fields), language=data.language, platform_id=platform.id)

            db.add(platform_data)

        db.commit()
        db.refresh(platform)

        return {'message': 'Platform created successfuly'}
    except Exception as e:
        db.rollback()
        if e.status_code == 422:
            raise e
        raise HTTPException(status_code=500, detail=str(e))

@route.put("/platforms/{id}", response_model=Dict[str, str])
def update_platform(id: int, request: Request, model: List[AdminPlatformSchema], db: Session = Depends(get_db), _user: dict = Depends(is_authenticated)):
    platform = db.query(Platform).filter(Platform.id == id).first()
    platform_datas = db.query(Platform_Data).filter(Platform_Data.platform_id == id)

    for data in platform_datas:
        selected_model = next(filter(lambda m: m.language == data.language, model), None)

       
        if selected_model:
            fields = {}
            values = {}
            for field in selected_model.fields:
                key, value = field.name, field.type
                fields[key] = value.value
                value[key] = ''

            if selected_model.name != None and selected_model.name != '':
                data.name = selected_model.name
            
            data.fields = json.dumps(fields)
            platform.status = selected_model.status
            
        else:
            raise HTTPException(status_code=400, detail="The requested platform doesn't exist")

    db.commit()

    return { 'message': 'Platform updated successfuly' }



@route.delete("/platforms/{id}")
def delete_platform(id: int, request: Request, db: Session = Depends(get_db), _user: dict = Depends(is_authenticated)):
    platform = db.query(Platform).filter(Platform.id == id).first()

    if platform == None:
        return {}

    platform_datas = db.query(Platform_Data).filter(Platform_Data.platform_id == platform.id).all()

    for data in platform_datas:
        db.delete(data)
        
    db.delete(platform)
    db.commit()

    return {}
