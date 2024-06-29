
from hashlib import sha1
from bson import ObjectId
from fastapi import APIRouter, Body
from db import db
from models import Pangkalan


pangkalan_router = APIRouter()


@pangkalan_router.get('/pangkalan')
def get_pangkalan(search: str | None = None, tanpa_foto: str | None = 'false'):
    queries = {}

    if search is not None and len(search) > 0:
        queries = {'$text': {'$search': search}}

    options = {}
    if tanpa_foto == 'true':
        options = {"foto": 0}

    try:
        pangkalan = list(db.pangkalan.find(queries, options))

        for x in pangkalan:
            x['_id'] = str(x['_id'])

        return {'status': 'success', 'pangkalan': pangkalan}
    except Exception as e:
        return {'status': 'failed', 'message': str(e)}


# @pangkalan_router.get('/pangkalan/{id}')
# def get_pangkalan_by_id(id: str):
#     try:
#         pangkalan = db.pangkalan.find_one({'_id': ObjectId(id)})

#         if pangkalan == None:
#             return {'status': 'failed', 'pangkalan': pangkalan, 'message': 'Pangkalan tidak ditemukan'}

#         pangkalan['_id'] = str(pangkalan['_id'])

#         return {'status': 'success', 'pangkalan': pangkalan}
#     except Exception as e:
#         return {'status': 'failed', 'message': str(e)}
    
@pangkalan_router.get('/pangkalan/{email}')
def get_pangkalan_by_email(email: str):
    try:
        pangkalan = db.pangkalan.find_one({'email': email})

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


@pangkalan_router.delete('/pangkalan/{id}')
def delete_pangkalan(id: str):
    try:
        response = db.pangkalan.delete_one({'_id': ObjectId(id)})

        if response.deleted_count == 0:
            return {'status': 'failed', 'message': 'Pangkalan tidak ditemukan'}

    except Exception as e:
        return {'status': 'failed', 'message': str(e)}
    else:
        return {'status': 'success'}


@pangkalan_router.patch('/pangkalan/ganti-kata-sandi/{email}')
def ganti_kata_sandi(email: str, kata_sandi: str = Body(embed=True)):
    hashed_kata_sandi = sha1()
    hashed_kata_sandi.update(kata_sandi.encode('utf-8'))
    kata_sandi = hashed_kata_sandi.hexdigest()

    try:
        response = db.pangkalan.update_one(
            {'email': email},
            {"$set": {'kata_sandi': kata_sandi}}
        )

        if response.matched_count == 0:
            return {'status': 'failed', 'message': 'Pangkalan tidak ditemukan'}

        return {'status': 'success'}
    except Exception as e:
        return {'status': 'failed', 'message': str(e)}
