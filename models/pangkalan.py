from pydantic import BaseModel


class Pangkalan(BaseModel):
    nama: str
    alamat: str
    harga: int
    email: str
    telepon: str
    gmap: str
    ulasan: dict | None = {}
