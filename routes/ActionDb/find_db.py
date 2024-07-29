import os

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

from database import Database as db
from models.ActionDb import find_one

# Criação do roteador para as rotas do FastAPI
router = APIRouter()
load_dotenv()  # Carrega as variáveis de ambiente do arquivo .env

# Carregando as mensagens de retorno do arquivo .env
ITEM_NOT_FOUND = os.getenv("ITEM_NOT_FOUND")
SUCCESS_REGISTER_MSG = os.getenv("SUCCESS_REGISTER_MSG")


@router.post("/")
async def find(data: find_one):
    """
    Busca um documento em uma coleção especificada no banco de dados.

    Esta função recebe os dados de uma requisição POST, verifica se o item existe
    na coleção especificada e, se existir, retorna o documento. Se o item não for encontrado,
    retorna um erro.

    Parameters:
        data (find_one): Dados da requisição contendo a coleção e o ID do item a ser buscado.

    Returns:
        JSONResponse: Resposta JSON contendo o status da operação e o documento encontrado ou uma mensagem de erro.
    """
    
    # Converte os dados do objeto `find_one` para um dicionário
    doc = data.model_dump()

    # Verifica se o item existe na coleção especificada
    item_existing = await db.DataBase.find_in_db(
            collection_str=doc["collection"], id=doc["id"]
        )

    if item_existing:
            # Converte o ObjectId para string no documento encontrado
            payload = db.convert_object_id_to_str(item_existing)
            return JSONResponse(
                content={
                    "status": "OK",
                    "response": payload,
                },
                status_code=200,
            )

    # Se o item não for encontrado, retorna uma mensagem de erro
    return JSONResponse(
            content={
                "status": "ERROR",
                "response": {"code": ITEM_NOT_FOUND},
            },
            status_code=404,
        )
