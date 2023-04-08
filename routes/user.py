from fastapi import APIRouter, HTTPException, Depends, Request
from models.user import User 
from config.db import conn 
from schemas.user import serializeDict, serializeList
import re
from typing import Optional, Literal
from pydantic import BaseModel
from schemas.user import generate_employeeId
from datetime import datetime
import pymongo
from jose import JWTError, jwt

user = APIRouter() 

SECRET_KEY = "secret_key"
ALGORITHM = "HS256"

async def get_auth_cookie(request: Request):
    authorization = request.cookies.get("Authorization")
    print(f"Authorization cookie: {authorization}")
    if not authorization:
        raise HTTPException(status_code=401, detail='Authorization cookie is missing or invalid')
    try:
        scheme, token = authorization.split()
        cleaned_token = token.strip("b'").strip("'")
        if scheme != "Bearer":
            raise HTTPException(status_code=401, detail='Authorization cookie is missing or invalid')
        decoded_jwt = jwt.decode(cleaned_token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"Decoded JWT: {decoded_jwt}")
        return decoded_jwt
    except (JWTError, ValueError):
        raise HTTPException(status_code=401, detail='Authorization cookie is missing or invalid')

@user.get('/api/getEmpByEmployeeId/{employeeId}')
async def getEmpByEmployeeId(employeeId: int, auth_cookie: str = Depends(get_auth_cookie)):
    return serializeDict(conn.local.user.find_one({"employeeId": employeeId}))

@user.get('/api/getEmpByAll/') 
async def getEmpByStatus(status: Optional[str] = "", auth_cookie: str = Depends(get_auth_cookie)):
    if status == "":
        return serializeList(conn.local.user.find())
    elif status not in ["Active", "Inactive", "Deleted"]:
        raise HTTPException(status_code=400, detail="Status must be either Active, Inactive or Deleted")
    else:
        return serializeList(conn.local.user.find({"status": status}))


counterValue = 100000

@user.post('/api/createEmployee/')
async def createEmployee(user: User, auth_cookie: str = Depends(get_auth_cookie)):
    email = user.email
    try:
        user.age = int(user.age)
    except ValueError:
        raise HTTPException(status_code=400, detail='Age should be an integer')

    if not re.match(r"[^@]+@[^@]+\.[^@]+", user.email):
        raise HTTPException(status_code=400, detail='Invalid email address')

    if conn.local.user.find_one({"email": email}):
        raise HTTPException(status_code=400, detail="Email already exists in the database")

    if user.status not in ["Active", "Inactive", "Deleted"]:
        raise HTTPException(status_code=400, detail="Status must be either Active or Inactive")

    # Add creation date
    creation_date = datetime.now().strftime("%Y-%m-%d")
    user_dict = dict(user)
    user_dict['creationDate'] = creation_date
    

    employee = conn.local.user.find_one(sort=[("employeeId", pymongo.DESCENDING)])
    if employee is not None:
        last_employee_id = int(employee['employeeId'])
        user_dict['employeeId'] = generate_employeeId(last_employee_id)
    else:
         user_dict['employeeId'] = generate_employeeId(counterValue)
    conn.local.user.insert_one(user_dict)   

    return serializeList(conn.local.user.find()) 

class UserUpdate(BaseModel):
    name: Optional[str]
    age: Optional[int]
    designation: Optional[str]
    status: Optional[Literal["Active", "Inactive", "Deleted"]]

@user.put('/api/updateEmployee/{employeeId}')
async def updateEmployee(employeeId: int, user: UserUpdate, auth_cookie: str = Depends(get_auth_cookie)):
    # Ensure the email field is not being updated
    if hasattr(user, 'email'):
        raise HTTPException(status_code=400, detail='Email cannot be updated')

    updation_date = datetime.now().strftime("%Y-%m-%d")

    conn.local.user.find_one_and_update(
        {"employeeId": employeeId},
        {"$set": { "updationDate": updation_date, **user.dict(exclude_unset=True) }}
    )
    return serializeDict(conn.local.user.find_one({"employeeId": employeeId}))


@user.delete('/api/deleteEmployee/{employeeId}')
async def deleteEmployee(employeeId: int, user: User, auth_cookie: str = Depends(get_auth_cookie)):
    query = {"employeeId": employeeId}
    update = {"$set": {"status": "Deleted"}}
    result = conn.local.user.update_one(query, update)
    if result.modified_count > 0:
        return {"message": "Employee deleted successfully"}
    else:
        return {"message": "No employee found with the given ID"}


@user.delete('/api/deleteEmployeeAll/')
async def deleteEmployeeAll(auth_cookie: str = Depends(get_auth_cookie)):
    result = conn.local.user.delete_many({})
    if result.deleted_count == 0:
        return {"message": "No users found in the database."}
    else:
        return {"message": f"{result.deleted_count} user(s) deleted successfully."}