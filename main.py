from datetime import datetime, timedelta
import os
import time
import random
from hashlib import sha1
import ssl
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
from pymongo import MongoClient
from bson import ObjectId
from fastapi import FastAPI, Body
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from typing import Annotated
from models import Pengguna


load_dotenv()
database_password = os.getenv('DATABASE_PASSWORD')
email_address = os.getenv('EMAIL_ADDRESS')
email_password = os.getenv('EMAIL_PASSWORD')

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

db = MongoClient(
    f'mongodb+srv://mdaffailhami:{database_password}@cluster0.xidkjt2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
).gasku
db.pengguna.create_index('nik', unique=True)


@app.get("/")
async def main():
    return FileResponse('pages/index.html')


@app.get('/pengguna')
def get_pengguna():
    pengguna = list(db.pengguna.find())

    for x in pengguna:
        x['_id'] = str(x['_id'])

    return {'status': 'success', 'pengguna': pengguna}


@app.get('/pengguna/{nik}')
def get_pengguna_by_nik(nik: str):
    pengguna = db.pengguna.find_one({'nik': nik})

    if pengguna == None:
        return {'status': 'failed', 'pengguna': pengguna, 'message': 'Pengguna tidak ditemukan'}

    pengguna['_id'] = str(pengguna['_id'])

    return {'status': 'success', 'pengguna': pengguna}


@app.post('/pengguna')
def add_pengguna(pengguna: Pengguna):
    hashed_kata_sandi = sha1()
    hashed_kata_sandi.update(pengguna.kata_sandi.encode('utf-8'))
    pengguna.kata_sandi = hashed_kata_sandi.hexdigest()

    try:
        id = db.pengguna.insert_one(pengguna.__dict__).inserted_id
    except Exception as e:
        return {'status': 'failed', 'message': str(e)}
    else:
        return {'status': 'success', 'Inserted ID': str(id)}


@app.put('/pengguna/{id}')
def update_pengguna(id: str, pengguna: Pengguna):
    hashed_kata_sandi = sha1()
    hashed_kata_sandi.update(pengguna.kata_sandi.encode('utf-8'))
    pengguna.kata_sandi = hashed_kata_sandi.hexdigest()

    db.pengguna.update_one({'_id': ObjectId(id)}, {"$set": pengguna.__dict__})
    return {'status': 'success'}


@app.put('/ganti-kata-sandi/{id}')
def ganti_kata_sandi(id: str, kata_sandi: Annotated[str, Body()]):
    hashed_kata_sandi = sha1()
    hashed_kata_sandi.update(kata_sandi.encode('utf-8'))
    kata_sandi = hashed_kata_sandi.hexdigest()

    db.pengguna.update_one(
        {'_id': ObjectId(id)},
        {"$set": {'kata_sandi': kata_sandi}}
    )
    return {'status': 'success'}


@app.post('/kirim-email-verifikasi/{receiver}')
def kirim_email_verifikasi(receiver: str):
    em = EmailMessage()
    em['From'] = email_address
    em['To'] = receiver
    em['subject'] = 'Verifikasi GasKu'

    code = str(random.randint(10000, 99999))
    em.set_content(f'Kode verikasi kamu adalah {code}')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=ssl.create_default_context()) as smtp:
        smtp.login(email_address, email_password)
        smtp.sendmail(email_address, receiver, em.as_string())

        return {'status': 'success', 'kode_verifikasi': code}


@app.get('/konfirmasi-e-tiket/{nik}/{key}')
def konfirmasi_e_tiket_page():
    return FileResponse('pages/konfirmasi-e-tiket.html')


@app.post('/konfirmasi-e-tiket/{nik}/{key}')
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
