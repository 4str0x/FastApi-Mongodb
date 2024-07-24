import os

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from bson import ObjectId  

from database import Database as db
from package import JwtBarrer
from models.ActionDb import find_one

router = APIRouter()
load_dotenv()

ITEM_NOT_FOUND = os.getenv("ITEM_NOT_FOUND")
SUCCESS_REGISTER_MSG = os.getenv("SUCCESS_REGISTER_MSG")

@router.post("/", dependencies=[Depends(JwtBarrer.JWTBearer())])
async def find(data: find_one):
    doc = data.model_dump()
    item_existing = await db.DataBase.Find_in_db(collection_str=doc["collection"], id=doc["id"])

    if item_existing:
        payload = db.convert_object_id_to_str(item_existing)
        return JSONResponse(
            content={
                "status": "OK",
                "response": payload,
            },
            status_code=200,  
        )

    return JSONResponse(
        content={
            "status": "ERROR",
            "response": {"code": ITEM_NOT_FOUND},
        },
        status_code=404, 
    )
