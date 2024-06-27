from fastapi import APIRouter
from fastapi.responses import FileResponse

pages_router = APIRouter()


@pages_router.get("/")
def index():
    return FileResponse('pages/index.html')


@pages_router.get("/form-code")
def form_code():
    return FileResponse('pages/formCode.html')


@pages_router.get("/form-keluhan")
def form_keluhan():
    return FileResponse('pages/formKeluhan.html')


@pages_router.get("/form-login")
def form_login():
    return FileResponse('pages/formLogin.html')


@pages_router.get("/form-lupa-password")
def form_lupa_password():
    return FileResponse('pages/formLupaPassword.html')


@pages_router.get("/form-riwayat")
def form_riwayat():
    return FileResponse('pages/formRiwayat.html')


@pages_router.get("/form-update")
def form_update():
    return FileResponse('pages/formUpdate.html')


@pages_router.get('/konfirmasi-e-tiket/{nik}/{key}')
def konfirmasi_e_tiket_page():
    return FileResponse('pages/konfirmasi-e-tiket.html')
