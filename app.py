from fastapi import FastAPI, Request
import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routers import table

app = FastAPI()
app.mount('/static' , StaticFiles(directory='static'), name='static') #เรียกใช้ข้อมูลใน static
template = Jinja2Templates(directory='templates') #เรียกใช้ข้อมูลในtemplate

app.include_router(
    table.router,
    prefix='/api', #กำหนด pathข้างหน้า path table
    tags=['table'], #
    responses={418: {"description": "I'm a teapot"}},
)
 
@app.get('/') #/หน้าแรก #get คือการเข้ามาหน้าเว็บๆนั้น
def index():
    return 'Hello'



@app.get('/dashboard')
def index(request: Request):
    return template.TemplateResponse('dashboard.html', context={'request': request})



@app.get('/aaa')
def index(request: Request):
    return template.TemplateResponse('aaa.html', context={'request': request})
    




if __name__ == '__main__':
    uvicorn.run('app:app', debug=True, port=8080)

    