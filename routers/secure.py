from urllib.parse import scheme_chars
from fastapi import APIRouter, Form, Request, UploadFile, File, Response
from fastapi.exceptions import HTTPException
from pyasn1_modules.rfc2459 import DisplayText
from pydantic import BaseModel
from typing import Optional
from pydantic.tools import T

from pyrebase.pyrebase import Auth
from starlette import responses
from auth.firebase import Config_firebase
from firebase_admin import auth
import json
import firebase_admin
from firebase_admin import credentials
import pyrebase
import os
from datetime import timedelta
from fastapi.responses import RedirectResponse
from auth.token_firebase import set_authentication, set_firebase

# with open('auth/firebase.json', 'r') as json_file:
#     load_json = json.load(json_file)
#     database = load_json['firebase']
#     authen = load_json['credential']

auth_file = credentials.Certificate(set_authentication)
firebase_admin.initialize_app(auth_file)
pb = pyrebase.initialize_app(set_firebase)
db = pb.database()


pb = pb.auth()
router = APIRouter()

@router.post('/register')
async def register(
        request: Request,
        file: Optional[UploadFile] = File(None),
        email: str = Form(...),
        password: str = Form(...),
        username: str = Form(...)
):
    host = request.url.hostname
    scheme =request.url.scheme
    port = request.url.port
    filename = file.filename
    http = f'{scheme}://{host}:{port}/static/uploads/{filename}'
    user = auth.create_user(
        email=email,
        password=password,
        display_name=username,
        photo_url=http
    )
    static_file = 'f/static/uploads/{file.filename}'
    with open(static_file, 'wb+') as upload_file:
        upload_file.write(file.file.read())
        upload_file.close()
    return {'user': user}



@router.post('/login')
async def login(
    response: Response,
    email: Optional[str] = Form(None),
    password: Optional[str] = Form(None),
    remember: Optional[list] = Form(None),
):
    try:
        user = pb.sign_in_with_email_and_password(email, password)
        check_verify = auth.get_user_by_email(user['email'])
        if check_verify.email_verified:
            expires = 60 * 60 * 1
            auth_cookie = auth.create_session_cookie(id_token=user['idToken'], expires_in=timedelta(hours=1))
            response.set_cookie(key='access-token', value=str(auth_cookie), expires=expires,)
            return {'url': '/dashboard', 'status': True}
        elif not check_verify.email_verified:
            pb.send_email_verification(user['idToken'])
            return {'status': False}
    except:
        raise HTTPException(status_code=403, detail='Email or Password Invalid')



@router.get('/logout')
async def get_cookies():
    response = RedirectResponse(url='/root_login')
    response.delete_cookie('access-token')
    return response



@router.get('/socket_auth')
async def socket_auth(request: Request):
    token = request.cookies.get('access-token')
    try:
        check = auth.verify_session_cookie(token)
        auth.revoke_refresh_tokens(check['sub'])
        return check
    except auth.InvalidSessionCookieError:
        raise HTTPException(status_code=403, detail={'description': 'Invalid'})



@router.post('/forgotpassword')
async def forgot(forgot: str = Form(...)):
    pb.send_password_reset_email(forgot)
    return 'success'