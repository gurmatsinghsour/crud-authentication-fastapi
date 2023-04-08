from fastapi import FastAPI, Request, Form, Cookie, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from bson import ObjectId
from passlib.context import CryptContext
from datetime import datetime, timedelta
import pymongo
import jwt
from jwt import PyJWTError
from routes.user import user



# MongoDB configuration
CONNECTION_STRING = "mongodb://localhost:27017/test"
client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database("local")
users_collection = db.get_collection("authentication")

# FastAPI configuration
app = FastAPI()
app.include_router(user)
templates = Jinja2Templates(directory="templates")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Models
class User(BaseModel):
    username: str
    password: str

class UserInDB(BaseModel):
    username: str
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str = None

# Hash password
def get_password_hash(password):
    return pwd_context.hash(password)

# Verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Create access token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Get user by username
def get_user(username: str):
    user = users_collection.find_one({"username": username})
    if user:
        return UserInDB(username=user['username'], hashed_password=user['hashed_password'])


# Get user by object id
def get_user_by_id(user_id: str):
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        return UserInDB(username=user['username'], hashed_password=user['hashed_password'])

# Get current user
async def get_current_user(token: str = Cookie(None)):
    if not token:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            return None
        token_data = TokenData(username=username)
    except PyJWTError:
        return None
    user = get_user(token_data.username)
    if user is None:
        return None
    return user

# Routes
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    user = await get_current_user(request.cookies.get("token"))
    return templates.TemplateResponse("index.html", {"request": request, "user": user})

@app.post("/signin")
async def signin(request: Request):
    form = await request.form()
    username = form.get("username")
    password = form.get("password")
    user = get_user(username)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    access_token = create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    response = JSONResponse(content={"message" : "Sign in sucessfull!"})
    response.set_cookie(key="Authorization", value=f"Bearer {access_token}", httponly=True, samesite="None", secure=True)
    return response

@app.post("/signup")
async def signup(username: str = Form(...), password: str = Form(...)):
    existing_user = get_user(username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(password)
    user = {"username": username, "hashed_password": hashed_password}
    users_collection.insert_one(user)
    return {"message": "User created successfully"}

@app.post("/successful", response_class=HTMLResponse)
async def successful():
    return {"message": "Successful"}

@app.get("/reset", response_class=HTMLResponse)
async def index(request: Request):
    user = await get_current_user(request.cookies.get("token"))
    return templates.TemplateResponse("reset_password.html", {"request": request, "user": user})

@app.post("/reset_password", response_class=HTMLResponse)
async def reset_password(request: Request):
    form = await request.form()
    username = form.get("username")
    current_password = form.get("current_password")
    new_password = form.get("new_password")
    
    if not (username and current_password and new_password):
        raise HTTPException(status_code=400, detail="Missing fields")
    
    user = get_user(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not verify_password(current_password, user.hashed_password):
        print(current_password)
        print(user.hashed_password)
        raise HTTPException(status_code=400, detail="Invalid password")
    
    new_hashed_password = get_password_hash(new_password)
    users_collection.update_one(
        {"username": username},
        {"$set": {"hashed_password": new_hashed_password}}
    )
    
    responseSuccess = JSONResponse(content={"message": "Password reset successful"})
    return responseSuccess


@app.get("/logout")
async def logout(request: Request):
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.delete_cookie(key="Authorization")
    return response

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8800)
