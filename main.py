from fastapi import FastAPI
from fastapi.responses import JSONResponse
from rotas import router

app = FastAPI(title="FastApi + Mongodb")

@app.get("/")
async def root():
    return JSONResponse(content={"status": "OK"}, status_code=200)

app.include_router(router, prefix="")

if __name__ == '__main__':
    import uvicorn
    
    uvicorn.run("main:app", host="", port=80)