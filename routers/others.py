from email.message import EmailMessage
import os
import random
import smtplib
import ssl
from fastapi import APIRouter

email_address = os.getenv('EMAIL_ADDRESS')
email_password = os.getenv('EMAIL_PASSWORD')

others_router = APIRouter()


@others_router.post('/kirim-email-verifikasi/{receiver}')
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
