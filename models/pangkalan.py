from datetime import datetime
from math import floor
from pydantic import BaseModel


class Pangkalan(BaseModel):
    nama: str
    alamat: str
    harga: int
    stok: int
    email: str
    telepon: str
    gmap: str
    coordinates: tuple[float, float]
    foto: list | None = []
    ulasan: dict | None = {}
