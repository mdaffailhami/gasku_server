
from hashlib import sha1
from bson import ObjectId
from fastapi import APIRouter, Body
from db import db
from models import Pangkalan


pangkalan_router = APIRouter()


@pangkalan_router.get('/pangkalan')
def get_pangkalan(search: str | None = None):
    try:
        pangkalan = list(
            db.pangkalan.find()
        ) if search is None else list(
            db.pangkalan.find({'$text': {'$search': search}})
        )

        for x in pangkalan:
            x['_id'] = str(x['_id'])

        return {'status': 'success', 'pangkalan': pangkalan}
    except Exception as e:
        return {'status': 'failed', 'message': str(e)}


@pangkalan_router.get('/pangkalan/{id}')
def get_pangkalan_by_id(id: str):
    try:
        pangkalan = db.pangkalan.find_one({'_id': ObjectId(id)})

        if pangkalan == None:
            return {'status': 'failed', 'pangkalan': pangkalan, 'message': 'Pangkalan tidak ditemukan'}

        pangkalan['_id'] = str(pangkalan['_id'])

        return {'status': 'success', 'pangkalan': pangkalan}
    except Exception as e:
        return {'status': 'failed', 'message': str(e)}


@pangkalan_router.post('/pangkalan')
def add_pangkalan(pangkalan: Pangkalan):
    hashed_kata_sandi = sha1()
    hashed_kata_sandi.update(pangkalan.kata_sandi.encode('utf-8'))
    pangkalan.kata_sandi = hashed_kata_sandi.hexdigest()

    try:
        id = db.pangkalan.insert_one(pangkalan.__dict__).inserted_id
    except Exception as e:
        return {'status': 'failed', 'message': str(e)}
    else:
        return {'status': 'success', 'Inserted ID': str(id)}


@pangkalan_router.patch('/pangkalan/{id}')
def update_pangkalan(id: str, data: dict = Body()):
    if 'kata_sandi' in data:
        hashed_kata_sandi = sha1()
        hashed_kata_sandi.update(data['kata_sandi'].encode('utf-8'))
        data['kata_sandi'] = hashed_kata_sandi.hexdigest()

    try:
        response = db.pangkalan.update_one(
            {'_id': ObjectId(id)}, {"$set": data}
        )

        if response.matched_count == 0:
            return {'status': 'failed', 'message': 'Pangkalan tidak ditemukan'}

    except Exception as e:
        return {'status': 'failed', 'message': str(e)}
    else:
        return {'status': 'success'}
