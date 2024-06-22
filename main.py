import os
from dotenv import load_dotenv
from pymongo import MongoClient
from fastapi import FastAPI
from hashlib import sha1
from email.message import EmailMessage
import ssl
import smtplib
from models.pengguna import Pengguna
from models.email import Email

load_dotenv()
database_password = os.getenv('DATABASE_PASSWORD')
email_address = os.getenv('EMAIL_ADDRESS')
email_password = os.getenv('EMAIL_PASSWORD')

app = FastAPI()
client = MongoClient(
    f'mongodb+srv://mdaffailhami:{database_password}@cluster0.xidkjt2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client.gasku


@app.post("/pengguna")
def add_user(pengguna: Pengguna):
    hashed_kata_sandi = sha1()
    hashed_kata_sandi.update(pengguna.kata_sandi.encode('utf-8'))
    pengguna.kata_sandi = hashed_kata_sandi.hexdigest()

    id = db.pengguna.insert_one(pengguna.__dict__).inserted_id
    return 'Inserted ID: ' + str(id)


@app.post('/send-email')
def send_email(email: Email):
    em = EmailMessage()
    em['From'] = email_address
    em['To'] = email.receiver
    em['subject'] = email.subject
    em.set_content(email.message)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=ssl.create_default_context()) as smtp:
        smtp.login(email_address, email_password)
        smtp.sendmail(email_address, email.receiver, em.as_string())
