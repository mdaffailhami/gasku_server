from datetime import datetime, timedelta
import os
import time
import random
from hashlib import sha1
import ssl
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
from pymongo import TEXT, MongoClient
from fastapi import FastAPI, Body
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from models import Pengguna
from models.pangkalan import Pangkalan


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
db.pangkalan.create_index(
    [('nama', TEXT), ('alamat', TEXT)], name='text_index')


@app.get("/")
async def main():
    return FileResponse('pages/index.html')


@app.get('/pengguna')
def get_pengguna():
    try:
        pengguna = list(db.pengguna.find())

        for x in pengguna:
            x['_id'] = str(x['_id'])

        return {'status': 'success', 'pengguna': pengguna}

    except Exception as e:
        return {'status': 'failed', 'message': str(e)}


@app.get('/pengguna/{nik}')
def get_pengguna_by_nik(nik: str):
    try:

        pengguna = db.pengguna.find_one({'nik': nik})

        if pengguna == None:
            return {'status': 'failed', 'pengguna': pengguna, 'message': 'Pengguna tidak ditemukan'}

        pengguna['_id'] = str(pengguna['_id'])

        return {'status': 'success', 'pengguna': pengguna}
    except Exception as e:
        return {'status': 'failed', 'message': str(e)}


@app.post('/pengguna')
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


@app.put('/pengguna/{nik}')
def update_pengguna(nik: str, pengguna: Pengguna):
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


@app.get('/pangkalan')
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


@app.get('/pangkalan/{id}')
def get_pangkalan_by_id(id: str):
    try:
        pangkalan = db.pangkalan.find_one({'_id': id})

        if pangkalan == None:
            return {'status': 'failed', 'pangkalan': pangkalan, 'message': 'Pangkalan tidak ditemukan'}

        pangkalan['_id'] = str(pangkalan['_id'])

        return {'status': 'success', 'pangkalan': pangkalan}
    except Exception as e:
        return {'status': 'failed', 'message': str(e)}


@app.post('/pangkalan')
def add_pangkalan(pangkalan: Pangkalan):
    try:
        id = db.pangkalan.insert_one(pangkalan.__dict__).inserted_id
    except Exception as e:
        return {'status': 'failed', 'message': str(e)}
    else:
        return {'status': 'success', 'Inserted ID': str(id)}


@app.put('/pangkalan/{id}')
def update_pangkalan(id: str, pangkalan: Pangkalan):
    try:

        response = db.pangkalan.update_one(
            {'_id': id}, {"$set": pangkalan.__dict__})

        if response.matched_count == 0:
            return {'status': 'failed', 'message': 'Pangkalan tidak ditemukan'}

    except Exception as e:
        return {'status': 'failed', 'message': str(e)}
    else:
        return {'status': 'success'}


@app.patch('/ganti-kata-sandi/{nik}')
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


@app.post('/kirim-email-verifikasi/{receiver}')
def kirim_email_verifikasi(receiver: str):
    em = EmailMessage()
    em['From'] = email_address
    em['To'] = receiver
    em['subject'] = 'Verifikasi GasKu'

    code = str(random.randint(10000, 99999))
    em.set_content(f'Kode verikasi kamu adalah {code}')

    smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465,
                            context=ssl.create_default_context())
    try:
        smtp.login(email_address, email_password)
        smtp.sendmail(email_address, receiver, em.as_string())

        return {'status': 'success', 'kode_verifikasi': code}
    except smtplib.SMTPRecipientsRefused as e:
        return {'status': 'failed', 'code': e.recipients[receiver][0], 'message': str(e)}
    finally:
        smtp.close()


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
