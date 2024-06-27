from datetime import datetime, timedelta
from hashlib import sha1
from fastapi import APIRouter, Body
from db import db
from models import Pengguna


pengguna_router = APIRouter()


@pengguna_router.get('/pengguna')
def get_pengguna():
    try:
        pengguna = list(db.pengguna.find())

        for x in pengguna:
            x['_id'] = str(x['_id'])

        return {'status': 'success', 'pengguna': pengguna}

    except Exception as e:
        return {'status': 'failed', 'message': str(e)}


@pengguna_router.get('/pengguna/{nik}')
def get_pengguna_by_nik(nik: str):
    try:

        pengguna = db.pengguna.find_one({'nik': nik})

        if pengguna == None:
            return {'status': 'failed', 'pengguna': pengguna, 'message': 'Pengguna tidak ditemukan'}

        pengguna['_id'] = str(pengguna['_id'])

        return {'status': 'success', 'pengguna': pengguna}
    except Exception as e:
        return {'status': 'failed', 'message': str(e)}


@pengguna_router.post('/pengguna')
def add_pengguna(pengguna: Pengguna):
    hashed_kata_sandi = sha1()
    hashed_kata_sandi.update(pengguna.kata_sandi.encode('utf-8'))
    pengguna.kata_sandi = hashed_kata_sandi.hexdigest()

    try:
        id = db.pengguna.insert_one(pengguna.__dict__).inserted_id
    except Exception as e:
        if e.code == 11000:
            return {'status': 'failed', 'message': 'NIK sudah terdaftar'}

        return {'status': 'failed', 'message': str(e)}
    else:
        return {'status': 'success', 'Inserted ID': str(id)}


@pengguna_router.put('/pengguna/{nik}')
def update_pengguna(nik: str, pengguna: Pengguna, hash: str | None = 'false'):
    if hash == 'true':
        hashed_kata_sandi = sha1()
        hashed_kata_sandi.update(pengguna.kata_sandi.encode('utf-8'))
        pengguna.kata_sandi = hashed_kata_sandi.hexdigest()

    try:

        response = db.pengguna.update_one(
            {'nik': nik}, {"$set": pengguna.__dict__})

        if response.matched_count == 0:
            return {'status': 'failed', 'message': 'Pengguna tidak ditemukan'}

        return {'status': 'success'}
    except Exception as e:
        return {'status': 'failed', 'message': str(e)}


@pengguna_router.patch('/ganti-kata-sandi/{nik}')
def ganti_kata_sandi(nik: str, kata_sandi: str = Body(embed=True)):
    print(kata_sandi)
    hashed_kata_sandi = sha1()
    hashed_kata_sandi.update(kata_sandi.encode('utf-8'))
    kata_sandi = hashed_kata_sandi.hexdigest()

    try:
        response = db.pengguna.update_one(
            {'nik': nik},
            {"$set": {'kata_sandi': kata_sandi}}
        )

        if response.matched_count == 0:
            return {'status': 'failed', 'message': 'Pengguna tidak ditemukan'}

        return {'status': 'success'}
    except Exception as e:
        return {'status': 'failed', 'message': str(e)}


@pengguna_router.post('/konfirmasi-e-tiket/{nik}/{key}')
def konfirmasi_e_tiket(nik: str, key: str):
    now = datetime.now()
    monday = now - timedelta(days=now.weekday())
    monday_formatted = monday.strftime('%d-%m-%Y')

    key_comparison = sha1()
    key_comparison.update(f'{nik}({monday_formatted})'.encode('utf-8'))
    key_comparison = key_comparison.hexdigest()

    if key == key_comparison:
        result = db.pengguna.update_one(
            {'nik': nik},
            {"$addToSet": {'riwayat_e_tiket': monday_formatted}}
        )

        if result.modified_count == 0:
            return {'status': 'failed', 'message': 'Gagal Mengkonfirmasi, Tiket Sudah Pernah Dikonfirmasi'}
        else:
            return {'status': 'success'}

    else:
        return {'status': 'failed', 'message': 'Wrong key'}
