from pydantic import BaseModel

class insert_one(BaseModel):
    collection: str
    payload: dict
    
class find_one(BaseModel):
    id: int
    collection: str
    
class update(BaseModel):
    id: int
    collection: str
    value: dict