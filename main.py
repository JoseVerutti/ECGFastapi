from fastapi import FastAPI, Path
from pydantic import BaseModel, conlist
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from deta import Deta  # Import Deta
from typing import  List
import json


#Establece conexion con la base de datos de DETA SPACE (liz)
DETA_PROJECT_KEY="e0qu1ysuqyb_uqwhLicX5BUf3rqumZ2w3KpBqSdsCDsc"

deta = Deta(DETA_PROJECT_KEY)

db = deta.Base("ECG")


#Crea el modelo
class ECG(BaseModel):
    la: conlist(int, min_length=300, max_length=300)
    ll: conlist(int, min_length=300, max_length=300)
    v1: conlist(int, min_length=300, max_length=300)
    

#Inicializa la api
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/ecg", response_model=ECG, status_code=201)
def postdatos(ecg: ECG)-> ECG:
    # el metodo fetch de la base de datos obtiene los datos especificados de esta.
    # Se conecta a la base de datos y obtiene el numero de la cantidad de datos que hay existentes. Le suma uno y almacena este valor en la variable key.
    key=int(db.fetch()._count)+1
    #El metodo put de la base de datos sube a esta los datos especificados (ecg).
    db.put(jsonable_encoder(ecg),str(key))
    #Envia una respuesta al consumidor de la api.
    return JSONResponse(status_code=201, content={"message":"Ok"})

@app.get("/ecg", response_model= List[ECG], status_code=200)
def getall() -> List[ECG]:

    #Trae todos los datos de la base de datos.
    response= db.fetch()
    #Aonvierte los datos a formato Json
    data=jsonable_encoder(response)
    #Almacena la cantidad de datos que hay en la api en count y todos los datos en la variable items.
    count = data["_count"]
    items = data["_items"]
    #En un bucle recorre todos los datos que trajo de la base de datos hasta encontrar el dato con key
    #igual a la cantidad de datos (Almacena el ultimo dato de la base de datos en la variable dato).
    dato= [item for item in items if item["key"] == str(count)]
    #Le responde al consumidor enviando la variable dato (El ultimo dato que se encuentra en la base de datos).
    return JSONResponse(status_code=200, content=jsonable_encoder(dato))

