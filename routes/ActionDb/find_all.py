import os
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from bson import json_util
from pymongo.cursor import Cursor

from database import Database as db
from package import JwtBarrer

router = APIRouter()
load_dotenv()

GENERIC_ERROR = os.getenv("GENERIC_ERROR")


@router.get("/", dependencies=[Depends(JwtBarrer.JWTBearer())])
async def find_all(collection: str):
    result =  await db.DataBase.find_all(collection_str=collection)
    
    if collection == "Token" or collection == "SystemCrips":
        return JSONResponse(
            content={
                "status": "Erro",
                "response": "access to this collection denied"},
                status_code=403,
            )
    
    
    if result == GENERIC_ERROR:
        return JSONResponse(
            content={
                "status": "ERROR",
                "response": {"code": GENERIC_ERROR},
            },
            status_code=500,
        )
        
    return JSONResponse(
        content={
            "status": "OK",
            "response": result,
            },
            status_code=200,
        )
    
    
