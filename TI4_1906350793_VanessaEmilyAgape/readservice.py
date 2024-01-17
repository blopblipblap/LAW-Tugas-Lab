from fastapi import FastAPI
from pydantic import BaseModel
import sqlalchemy
import databases

app = FastAPI()

mahasiswaDB = {}

DATABASE_URL = "sqlite:///./mahasiswa.db"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

mahasiswas = sqlalchemy.Table(
    "mahasiswas",
    metadata,
    sqlalchemy.Column("npm", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("nama", sqlalchemy.String),
)

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)

class Mahasiswa(BaseModel):
    npm: int
    nama: str

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

class Mahasiswa(BaseModel):
    npm: int
    nama: str

@app.get("/read/{npm}")
async def mahasiswa_get(npm: int):
    #query = sqlalchemy.select(mahasiswas.c.npm)
    query = sqlalchemy.select(mahasiswas).where(mahasiswas.c.npm == npm)
    mahasiswaSekarang = await database.fetch_one(query)
    return {"status":"OK", "npm":mahasiswaSekarang.npm, "nama":mahasiswaSekarang.nama}