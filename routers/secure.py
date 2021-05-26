
from fastapi import APIRouter, Form, Request, UploadFile, File, Response
from pydantic import BaseModel
from typing import Optional
from starlette import responses
from firebase_admin import auth, credentials
import json
import firebase_admin
import pyrebase
import os
from datetime import timedelta
from fastapi.responses import RedirectResponse

import os

router = APIRouter()

set_firebase = {
    "apiKey": os.environ['apiKey'],
    "authDomain": os.environ['authDomain'],
    "projectId": os.environ['projectId'],
    "databaseURL": os.environ['databaseURL'],
    "storageBucket": os.environ['storageBucket'],
    "messagingSenderId": os.environ['messagingSenderId'],
    "appId": os.environ['appId'],
    "measurementId": os.environ['measurementId']
}

set_authentication = {
    "type": os.environ['type'],
    "project_id": os.environ['project_id'],
    "private_key_id": os.environ['private_key_id'],
    "private_key": os.environ['private_key'].replace("\\n", "\n"),
    "client_email": os.environ['client_email'],
    "client_id": os.environ['client_id'],
    "auth_uri": os.environ['auth_uri'],
    "token_uri": os.environ['token_uri'],
    "auth_provider_x509_cert_url": os.environ['auth_provider_x509_cert_url'],
    "client_x509_cert_url": os.environ['client_x509_cert_url']
}


class Config_firebase:
    def __init__(self, path_db, path_auth):
        self.path_db = path_db
        self.path_auth = credentials.Certificate(path_auth)
        firebase_admin.initialize_app(self.path_auth)

    def authentication(self):
        firebase = self.path_db
        pb = pyrebase.initialize_app(firebase).auth()
        return pb
    def database_fb(self):
        firebase = self.path_db
        config = pyrebase.initialize_app(firebase)
        db = config.database()
        return db



config = Config_firebase(path_db=set_firebase, path_auth=set_authentication)
pb = config.authentication()
db = config.database_fb()

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