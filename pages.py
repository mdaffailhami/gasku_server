from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()


@router.get("/")
def index():
    return FileResponse('pages/index.html')


@router.get("/form-code")
def form_code():
    return FileResponse('pages/formCode.html')


@router.get("/form-keluhan")
def form_keluhan():
    return FileResponse('pages/formKeluhan.html')


@router.get("/form-login")
def form_login():
    return FileResponse('pages/formLogin.html')


@router.get("/form-lupa-password")
def form_lupa_password():
    return FileResponse('pages/formLupaPassword.html')


@router.get("/form-riwayat")
def form_riwayat():
    return FileResponse('pages/formRiwayat.html')


@router.get("/form-update")
def form_update():
    return FileResponse('pages/formUpdate.html')


@router.get('/konfirmasi-e-tiket/{nik}/{key}')
def konfirmasi_e_tiket_page():
    return FileResponse('pages/konfirmasi-e-tiket.html')
