from fastapi import APIRouter, Body, Path
from firebase_db import db
from typing import Optional
from datetime import time
import datetime

router = APIRouter()

_d = datetime.datetime.now()

data =[
    {
        'user': 'A',
        'date': '13/02/2018',
        'time': '15:30:15',
        'todo': 'ผักโต'
    },
    {
        'user': 'B',
        'date': '23/02/2018',
        'time': '12:12:12',
        'todo': 'ผักสวยงาม'
    },
    {
        'user': 'C',
        'date': '01/03/2018',
        'time': '14:22:11',
        'todo': 'ผักโตเต็มที่'
    }
]

#data = [
#    {
#        'datetime': _d.strftime('%d/%m/%y'),
#        'time': _d.strftime('%H:%M:%S')
#    }
#]


@router.get('/table') #get เรัยกข้อมูลมาดู
def table_get():
    return data

@router.post('/table') #post บันทึกข้อมูล
def table_post(payload: Optional[dict] = Body(None)):
    data.append(payload)
    return payload

@router.put('/table/{id}') #put อัพเดทข้อมูล {ใส่ pathด้านหลัง มาใช้เป็นตัวแปร}
def table_update(
    id: Optional[str] = Path(None),
    payload: Optional[dict] = Body(None)):
    for i in data:
        if i['id'] == id:
            i['name'] = payload['name']
            return i

@router.delete('/table/{id}') #delete ลบข้อมูล
def table_delete(id: Optional[str] = Path(None)):
    id = int(id) - 1
    data.pop(int(id))
    return data