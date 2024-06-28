from pydantic import BaseModel


class LaporanPangkalan(BaseModel):
    nim_pelapor: str
    nama_pelapor: str
    id_pangkalan: str
    nama_pangkalan: str
    tanggal: str
    deskripsi: str
