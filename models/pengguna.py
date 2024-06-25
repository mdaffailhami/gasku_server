from pydantic import BaseModel


class Pengguna(BaseModel):
    nama: str
    email: str
    nik: str
    kk: str
    kata_sandi: str
    foto: str | None = None
    riwayat_e_tiket: list | None = []
