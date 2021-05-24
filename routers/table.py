from fastapi import APIRouter, Body, Path, HTTPException
# from firebase_db import db
from typing import Optional
from datetime import time
from pydantic import BaseModel
import datetime
import uuid


router = APIRouter()



data =[
    {
        'id': 42152,
        'user': 'A',
        'date': '13/02/2018',
        'time': '15:30:15',
        'todo': 'ผักโต'
    },
    {
        'id': 52453,
        'user': 'B',
        'date': '23/02/2018',
        'time': '12:12:12',
        'todo': 'ผักสวยงาม'
    },
    {
        'id': 54353,
        'user': 'C',
        'date': '01/03/2018',
        'time': '14:22:11',
        'todo': 'ผักโตเต็มที่'
    }
]



class Item(BaseModel): #รับข้อมูลมาจากหน้าบ้าน
    user: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None
    todo: Optional[str] = None

    

@router.get('/table') #get เรัยกข้อมูลมาดู
async def table_get():
    return data[::-1] #เอาข้อมูลล่าสุด

@router.post('/table', status_code=201) #post บันทึกข้อมูล
async def table_post(item: Item):
    try:
        key = uuid.uuid4().hex
        _d = datetime.datetime.now()
        item = item.dict()
        item["date"] = _d.strftime("%d/%m/%y")
        item["time"] = _d.strftime("%H:%M:%S")
        item["id"] = key
        print(item)
        data.append(item)
        return item
    except:
        raise HTTPException(status_code=400, detail='someting weng wrong!')

@router.put('/table/{id}') #put อัพเดทข้อมูล {ใส่ pathด้านหลัง มาใช้เป็นตัวแปร}
async def table_update(
    item: Item,
    id: Optional[str] = Path(None)
):
    payload = item.dict()
    _d = datetime.datetime.now()
    for i in data:
        if i['id'] == id:
            i['todo'] = payload['todo']
            i['date'] = _d.strftime("%d/%m/%y")
            i['time'] = _d.strftime("%H:%M:%S")
            return i

@router.delete('/table/{id}') #delete ลบข้อมูล
async def table_delete(id: Optional[str] = Path(None)):
    id = int(id) - 1
    data.pop(int(id))
    return data