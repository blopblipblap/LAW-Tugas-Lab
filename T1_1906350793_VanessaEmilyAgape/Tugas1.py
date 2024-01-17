from typing import Optional
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request, Form, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel
from passlib.context import CryptContext
import datetime
import random
import string

class UnicornException(Exception):
    def __init__(self, pesan: str):
        self.pesan = pesan

class User(BaseModel):
    username: str
    full_name: Optional[str] = None
    npm: Optional[str] = None

class UserInDB(User):
    password: str

users_db = {
    "vanessa.emily": {
        "username": "vanessa.emily",
        "password": "$2b$12$OyMAFusGLJOqovZJORKZeuvQ//YmUuwN1Q/5fJTiEeQc0ULeE1kUq",
        "full_name": "Vanessa Emily Agape",
        "npm": "1906350793",
        "client_id": "7162",
        "client_secret": "1231"
    },
}

session = {
    "access_token" : "",
    "refresh_token": "",
    "user": "",
    "client_id": "",
    "ACCESS_TOKEN_EXPIRE": 0,
    "REFRESH_TOKEN_EXPIRE": 0
}

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

security = HTTPBearer()

@app.exception_handler(UnicornException)
async def unicorn_exception_handler_satu(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=401,
        content={
            "error":"invalid_request",
            "Error_description":exc.pesan,
        }
    )

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user(username: str):
    if username in users_db:
        user_dict = users_db[username]
        return UserInDB(**user_dict)

def get_password_hash(password):
    return pwd_context.hash(password)

def check_user(username: str, password: str):
    if username not in users_db:
        return 1
    user = get_user(username)
    if not verify_password(password, user.password):
        return 2

def random_character(length):
    pool = string.ascii_letters + string.digits
    return ''.join(random.choice(pool) for i in range(length))

@app.post("/oauth/token")
async def token(
    username: str = Form(...),
    password: Optional[str] = Form(None),
    grant_type: str = "password",
    client_id: Optional[str] = Form(None),
    client_secret: Optional[str] = Form(None) ):

    if session["REFRESH_TOKEN_EXPIRE"] == 0:
        if password == None or client_id == None or client_secret == None:
            raise UnicornException(pesan="Mohon masukan credentials")

        user_is_here = check_user(username=username, password=password)
        if user_is_here == 1:
            raise UnicornException(pesan="Username tidak terdaftar")
        elif user_is_here == 2:
            raise UnicornException(pesan="Password salah")

        session["REFRESH_TOKEN_EXPIRE"] = datetime.datetime.now() + datetime.timedelta(minutes=10)
        session['user'] = username
        session['client_id'] = client_id

    if datetime.datetime.now() < session["REFRESH_TOKEN_EXPIRE"]:
        access_token = random_character(40)
        refresh_token = random_character(40)
        session["REFRESH_TOKEN_EXPIRE"] = datetime.datetime.now() + datetime.timedelta(minutes=10)
        session["ACCESS_TOKEN_EXPIRE"] = datetime.datetime.now() + datetime.timedelta(minutes=5)
        session['access_token'] = access_token
        session['refresh_token'] = refresh_token

    else:
        if password == None or client_id == None or client_secret == None:
            raise UnicornException(pesan="Mohon masukan credentials")
        user_is_here = check_user(username=username, password=password)
        if user_is_here == 1:
            raise UnicornException(pesan="Username tidak terdaftar")
        elif user_is_here == 2:
            raise UnicornException(pesan="Password salah")
        access_token = random_character(40)
        refresh_token = random_character(40)
        session["REFRESH_TOKEN_EXPIRE"] = datetime.datetime.now() + datetime.timedelta(minutes=10)
        session["ACCESS_TOKEN_EXPIRE"] = datetime.datetime.now() + datetime.timedelta(minutes=5)
        session['access_token'] = access_token
        session['refresh_token'] = refresh_token
        session['user'] = username
        session['client_id'] = client_id

    return {
        "access_token": session['access_token'],
        "expires_in": 300,
        "token_type": "Bearer",
        "scope": "",
        "refresh_token": session['refresh_token'],
        }


@app.post("/oauth/resource")
async def resource(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    if token != session['access_token']:
        raise UnicornException(pesan="Access Token salah")

    if datetime.datetime.now() > session["ACCESS_TOKEN_EXPIRE"]:
        raise UnicornException(pesan="Access Token expired")

    username = session["user"]
    user = get_user(username=username)

    return {
        "access_token": session['access_token'],
        "client_id": session['client_id'],
        "user_id": user.username,
        "full_name": user.full_name,
        "npm": user.npm,
        "expires": 300,
        "refresh_token": session['refresh_token']
    }
    

    