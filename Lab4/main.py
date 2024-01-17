import os
import aiofiles as aiofiles
from ast import Str
from typing import Optional
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()

kegiatanDB = {}

try:
    os.makedirs("files")
except:
    pass

class Kegiatan(BaseModel):
    id: int
    judul: str
    deskripsi: str
    pembuat: str

class gantiKegiatan(BaseModel) :
    judul: Optional[str] = None
    deskripsi: Optional[str] = None

def error(message: str):
    return JSONResponse(status_code=401, content={'error-message': message})

@app.get("/kegiatan/{id}", response_model= Kegiatan)
def kegiatan_get(id: int):
    try:
        kegiatanSekarang = kegiatanDB[id]
    except:
        return error(f"Kegiatan {id} tidak ada")
    return kegiatanSekarang

@app.post("/kegiatan", response_model=Kegiatan)
def kegiatan_post(kegiatan: Kegiatan):
    if kegiatan.id in kegiatanDB:
        return error(f"Kegiatan {kegiatan.id} sudah ada")
    else:
        kegiatanBaru = Kegiatan(id=kegiatan.id, judul=kegiatan.judul, deskripsi=kegiatan.deskripsi, pembuat=kegiatan.pembuat)
        kegiatanDB[kegiatan.id] = kegiatanBaru
        return kegiatanBaru

@app.put("/kegiatan/{id}", response_model=Kegiatan)
def kegiatan_put(id:int, update: gantiKegiatan):
    try:
        kegiatanSekarang = kegiatanDB[id]
    except:
        return error(f"Kegiatan {id} tidak ada")
    if update.judul: kegiatanSekarang.judul = update.judul
    if update.deskripsi: kegiatanSekarang.deskripsi = update.deskripsi
    return kegiatanSekarang

@app.delete("/kegiatan/{id}")
def kegiatan_delete(id: int):
    try: 
        kegiatanSekarang = kegiatanDB[id]
    except:
        return error(f"Kegiatan {id} tidak ada")
    kegiatanDB.pop(id)
    return JSONResponse(status_code=200, content={'message': f'Delete kegiatan {id} berhasil'})

@app.post("/kegiatan/files")
async def kegiatan_files(file: UploadFile = File(...)):
    async with aiofiles.open(f"files/{file.filename}", 'wb') as fileout:
        content = await file.read()
        await fileout.write(content)
    return JSONResponse(status_code=200, content={'message': f'Upload file berhasil'})