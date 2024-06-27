import os
from pymongo import TEXT, MongoClient

database_url = os.getenv('DATABASE_URL')

db = MongoClient(database_url).gasku

db.pengguna.create_index('nik', unique=True)
db.pangkalan.create_index(
    [
        ('nama', TEXT),
        ('alamat', TEXT)
    ],
    name='text_index'
)
