

from fastapi import APIRouter

from routes.ActionDb import insert_in_db as insert_in_db
from routes.ActionDb import find_db as find_db
from routes.ActionDb import deleted as deleted
from routes.ActionDb import edit as edit
from routes.ActionDb import find_all as find_all

router = APIRouter()


router.include_router(insert_in_db.router, prefix='/db/insert')
router.include_router(find_db.router, prefix='/db/find')
router.include_router(deleted.router, prefix='/db/deleted')
router.include_router(edit.router, prefix='/db/edit')
router.include_router(find_all.router, prefix='/db/find/all')