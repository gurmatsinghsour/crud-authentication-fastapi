from typing import Optional, Literal


def generate_employeeId(employeeId_counter):
    employeeId_counter += 1
    return employeeId_counter

def userEntity(item) -> dict:
    return {
        "employeeId": str(item["_employeeId"]),
        "name": item["name"],
        "age": item["age"],
        "designation": item["designation"],
        "email": item["email"],
        "status": Optional[Literal["Active", "Inactive", "Deleted"]],
        "creationDate" : item["creationDate"],
        "updationDate" : item["updationDate"]
    }


def usersEntity(entity) -> list:
    return [userEntity(item) for item in entity]

def serializeDict(a) -> dict:
    return {**{i:str(a[i]) for i in a if i=='_id'},**{i:a[i] for i in a if i!='_id'}}

def serializeList(entity) -> list:
    return [serializeDict(a) for a in entity]