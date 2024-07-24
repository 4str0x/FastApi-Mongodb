import os

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

from database import Database as db
from package import JwtBarrer
from models.ActionDb import insert_one

router = APIRouter()
load_dotenv()

ALREADY_REGISTERED_MSG = os.getenv("ALREADY_REGISTERED_MSG")
SUCCESS_REGISTER_MSG = os.getenv("SUCCESS_REGISTER_MSG")
ID_NOT_FOUND = os.getenv("ID_NOT_FOUND")


@router.post("/", dependencies=[Depends(JwtBarrer.JWTBearer())])
async def insert(data: insert_one):
    doc = data.model_dump()
    
    if "id" not in doc["resp"]:
        return JSONResponse(
            content={
                "status": "Error",
                "code": "ID NOT FOUND IN THE DOCUMENT",
            },
            status_code=400,
        )

    data_existing = await db.DataBase.Find_in_db(
        collection_str=doc["collection"], id=doc["resp"]["id"]
    )

    print(doc["resp"])
    
    if data_existing is not None:
        return JSONResponse(
            content={
                "status": "Error",
                "code": ALREADY_REGISTERED_MSG,
            },
            status_code=409,
        )
    else:
        await db.DataBase.Insert_in_db(
            collection_str=doc["collection"],
            document=doc["resp"]
        )

        return JSONResponse(
            content={
                "status": "OK",
                "response": {"code": SUCCESS_REGISTER_MSG},
            },
            status_code=201,
        )