from fastapi import FastAPI, Request, Form
from pydantic import BaseModel

app = FastAPI()

class Angka(BaseModel):
    angka_1: int
    angka_2: int

@app.get("/")
def read_root():
    return {"Hello": "World"}
    
@app.get("/test/{angka_1}/{angka_2}")
def read_root(angka_1: int, angka_2: int, request: Request):
    return {"perkalian": angka_1*angka_2}

@app.post("/test-post/")
async def post(angka_1: int = Form(...), angka_2: int = Form(...)):
    return {"perkalian": angka_1*angka_2}

@app.post("/test-post-json/")
async def create_angka(angka: Angka):
    return angka.angka_1*angka.angka_2





    