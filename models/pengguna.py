from pydantic import BaseModel


class Pengguna(BaseModel):
    nama_lengkap: str
    email: str
    nik: str
    kk: str
    kata_sandi: str
