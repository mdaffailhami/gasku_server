from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import pages_router, pengguna_router, pangkalan_router, others_router


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(pages_router)
app.include_router(pengguna_router)
app.include_router(pangkalan_router)
app.include_router(others_router)
