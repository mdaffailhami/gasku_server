from pydantic import BaseModel


class LaporanPangkalan(BaseModel):
    jenis_laporan: str
    nik_pelapor: str
    nama_pelapor: str
    id_pangkalan: str
    nama_pangkalan: str
    tanggal: str
    deskripsi: str
