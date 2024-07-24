import os

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

from database import Database as db
from package import JwtBarrer
from models.ActionDb import find_one

router = APIRouter()
load_dotenv()

ITEM_DELETED_SUCCESSFULLY = os.getenv("ITEM_DELETED_SUCCESSFULLY")
ITEM_NOT_FOUND = os.getenv("ITEM_NOT_FOUND")


@router.post("/", dependencies=[Depends(JwtBarrer.JWTBearer())])
async def deleted(data: find_one):
    doc = data.model_dump()
    item_exiting = await db.DataBase.Find_in_db(
        collection_str=doc["collection"], id=doc["id"]
    )

    if item_exiting:
        await db.DataBase.Deleted_in_db(collection_str=doc["collection"], id=doc["id"])

        return JSONResponse(
            content={
                "status": "OK",
                "response": {"code": ITEM_DELETED_SUCCESSFULLY},
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
