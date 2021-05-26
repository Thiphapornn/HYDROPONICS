import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routers import table, secure, esp
from fastapi.responses import RedirectResponse
from routers.secure import auth
import time


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
template = Jinja2Templates(directory="templates")

app.include_router(
    table.router,
    prefix="/api",
    tags=["table"],
    responses={418: {"description": "I'm a teapot"}},
)

app.include_router(
    secure.router,
    prefix='/secure',
    tags=['secure'],
    responses={418: {"description": "I'm a teapot"}},
)


app.include_router(
    esp.router,
    prefix='/esp',
    tags=['esp'],
    responses={418: {"description": "I'm a teapot"}},
)


@app.get("/dashboard")
async def dashboard(request: Request):
    token = request.cookies.get('access-token')
    if not token:
        return RedirectResponse(url='/root_login')
    if token:
        try:
            check_session = auth.verify_session_cookie(token)
            auth.revoke_refresh_tokens(check_session['sub'])
            # pusher_client.trigger('secure', 'session', check_session)
            return template.TemplateResponse('dashboard.html', context={'request': request})
        except auth.RevokedSessionCookieError:
            return RedirectResponse(url='/root_login')
        except auth.InvalidSessionCookieError:
            return RedirectResponse(url='/root_login')
    return template.TemplateResponse("dashboard.html", context={"request": request})



@app.get('/')
@app.get('/root_login', tags=['Page'])
async def root_login(request: Request):
    return template.TemplateResponse('login.html', context={'request': request})


if __name__ == "__main__":
    uvicorn.run("app:app", port=9191, debug=True)


