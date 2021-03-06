from fastapi import APIRouter, Form, Request, UploadFile, File, Response, HTTPException
from typing import Optional
from firebase_admin import auth
from environ.config_db import Config_firebase
from environ.heroku_environ import set_firebase, set_authentication
# from environ.client import set_firebase, set_authentication
from datetime import timedelta
from fastapi.responses import RedirectResponse
import os

router = APIRouter()

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
    filename = file.filename
    upload_dir = os.path.join('static', 'uploads')
    file_input = os.path.join(upload_dir, file.filename)
    http = f'https://hydroponics-iot.herokuapp.com/static/uploads/{filename}'
    user = auth.create_user(
        email=email,
        password=password,
        display_name=username,
        photo_url=http
    )
    if file:
        with open(file_input, 'wb+') as upload_file:
            upload_file.write(file.file.read())
            upload_file.close()
    return {'user': 'ijf'}


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
            response.set_cookie(key='access-token', value=str(auth_cookie), expires=expires, )
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
