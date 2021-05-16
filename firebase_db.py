import pyrebase
import json
import firebase_admin
from firebase_admin import credentials

with open('config/firebase.json', 'r') as json_file:
    load_json = json.load(json_file)
    database = load_json['db']
    authen = load_json['authen']
    auth = credentials.Certificate(authen)
    firebase_admin.initialize_app(auth)
    pb = pyrebase.initialize_app(database)
    db = pb.database()


