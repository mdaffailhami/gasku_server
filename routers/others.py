from email.message import EmailMessage
import os
import random
import smtplib
import ssl
from fastapi import APIRouter

from models import LaporanPangkalan

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


@others_router.post('/lapor-pangkalan/')
def lapor_pangkalan(laporan: LaporanPangkalan):
    em = EmailMessage()
    em['From'] = email_address
    em['To'] = email_address
    em['subject'] = 'Laporan Pangkalan GasKu'

    code = str(random.randint(10000, 99999))
    content = f'''Jenis Laporan: {laporan.jenis_laporan}
Pelapor: {laporan.nama_pelapor} ({laporan.nim_pelapor})
Pangkalan: {laporan.nama_pangkalan} ({laporan.id_pangkalan})
Tanggal: {laporan.tanggal}
Deskripsi:
{laporan.deskripsi}'''

    em.set_content(content)

    smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465,
                            context=ssl.create_default_context())
    try:
        smtp.login(email_address, email_password)
        smtp.sendmail(email_address, email_address, em.as_string())

        return {'status': 'success', 'content': content}
    except smtplib.SMTPRecipientsRefused as e:
        return {'status': 'failed', 'code': e.recipients[email_address][0], 'message': str(e)}
    finally:
        smtp.close()
