import os

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

from database import Database as db
from models.ActionDb import insert_one

# Criação do roteador para as rotas do FastAPI
router = APIRouter()
load_dotenv()  # Carrega as variáveis de ambiente do arquivo .env

# Carregando as mensagens de retorno do arquivo .env
ALREADY_REGISTERED_MSG = os.getenv("ALREADY_REGISTERED_MSG")
SUCCESS_REGISTER_MSG = os.getenv("SUCCESS_REGISTER_MSG")
ID_NOT_FOUND = os.getenv("ID_NOT_FOUND")


@router.post("/")
async def insert(data: insert_one):
    """
    Insere um documento em uma coleção especificada no banco de dados.

    Esta função recebe os dados de uma requisição POST, verifica se o item já existe
    na coleção especificada e, se não existir, insere o novo documento. Se o item já
    estiver registrado ou o ID não for encontrado no documento, retorna um erro.

    Parameters:
        data (insert_one): Dados da requisição contendo a coleção e o documento a ser inserido.

    Returns:
        JSONResponse: Resposta JSON contendo o status da operação e uma mensagem de sucesso ou erro.
    """
    try:
        # Converte os dados do objeto `insert_one` para um dicionário
        doc = data.model_dump()

        # Verifica se o campo "id" está presente no documento
        if "id" not in doc["payload"]:
            return JSONResponse(
                content={
                    "status": "Error",
                    "code": ID_NOT_FOUND,
                },
                status_code=400,
            )

        # Verifica se o item já existe na coleção especificada
        data_existing = await db.DataBase.find_in_db(
            collection_str=doc["collection"], id=doc["payload"]["id"]
        )

        if data_existing is not None:
            return JSONResponse(
                content={
                    "status": "Error",
                    "code": ALREADY_REGISTERED_MSG,
                },
                status_code=409,
            )

        # Insere o novo documento na coleção especificada
        await db.DataBase.insert_in_db(collection_str=doc["collection"], document=doc["payload"])

        return JSONResponse(
            content={
                "status": "OK",
                "response": {"code": SUCCESS_REGISTER_MSG},
            },
            status_code=201,
        )
    except Exception as e:
        # Captura qualquer exceção e retorna uma mensagem de erro genérica
        raise HTTPException(status_code=500, detail=str(e))
