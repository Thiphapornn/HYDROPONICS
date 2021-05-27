from fastapi import APIRouter, Path, Request
from routers.secure import db

router = APIRouter()


@router.get('/')
def esp_relay(relays: int = None):
    db.child('smartFarm').child('relay').set({'relays': relays})
    return {'relay': relays}


@router.get('/sensor')
def esp_sensor():
    ref = db.child('smartFarm').child('sensor').get()
    return ref.val()
