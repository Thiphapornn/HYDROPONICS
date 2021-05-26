from fastapi import APIRouter, Body, Path, HTTPException
from typing import Optional
from datetime import time
from pydantic import BaseModel
import datetime
from db import MongoDB
from object_str import CutId
from bson import ObjectId
import os

router = APIRouter()

var_mongodb = os.environ.get('MONGODB_URI')
db = MongoDB(database_name='dashboard', uri=var_mongodb)
collection = 'users'


class Item(BaseModel): #รับข้อมูลมาจากหน้าบ้าน
    user: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None
    todo: Optional[str] = None

    

@router.get('/table') #get เรัยกข้อมูลมาดู
async def table_get():
    data = db.find(collection=collection, query={})
    data = list(data)
    for k in data:
        del k['_id']
    return data[::-1] #เอาข้อมูลล่าสุด


@router.post('/table', status_code=201) #post บันทึกข้อมูล
async def table_post(item: Item):
    print(item)
    try:
        key = CutId(_id=ObjectId()).dict()['id']
        item = item.dict()
        _d = datetime.datetime.now()
        item["date"] = _d.strftime("%d/%m/%y")
        item["time"] = _d.strftime("%H:%M:%S")
        item["id"] = key
        db.insert_one(collection=collection, data=item)
        del item['_id']
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
    query = {'id': id}
    payload['date'] = _d.strftime("%d/%m/%y")
    payload['time'] = _d.strftime("%H:%M:%S")
    values = {'$set': payload}
    db.update_one(collection=collection, values=values, query=query)
    return 'success'
     

@router.delete('/table/{id}') #delete ลบข้อมูล
async def table_delete(id: Optional[str] = Path(None)):
    db.delete_one(collection=collection, query={'id': id})
    return 