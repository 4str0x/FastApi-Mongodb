import os

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

from database import Database as db
from models.ActionDb import find_one

# Criação do roteador para as rotas do FastAPI
router = APIRouter()
load_dotenv()

# Carregando as mensagens de retorno do arquivo .env
ITEM_DELETED_SUCCESSFULLY = os.getenv("ITEM_DELETED_SUCCESSFULLY")
ID_NOT_FOUND = os.getenv("ID_NOT_FOUND")


@router.post("/")
async def deleted(data: find_one):
    """
    Deleta um documento de uma coleção especificada no banco de dados.

    Esta função recebe os dados de uma requisição POST, verifica se o item existe
    na coleção especificada e, se existir, o deleta. Se o item não for encontrado,
    retorna um erro.

    Parameters:
        data (find_one): Dados da requisição contendo a coleção e o ID do item a ser deletado.

    Returns:
        JSONResponse: Resposta JSON contendo o status da operação e uma mensagem de sucesso ou erro.
    """
    try:
        # Converte os dados do objeto `find_one` para um dicionário
        doc = data.model_dump()

        # Verifica se o item existe na coleção especificada
        item_exiting = await db.DataBase.find_in_db(
            collection_str=doc["collection"], id=doc["id"]
        )

        if item_exiting:
            # Se o item existir, deleta-o da coleção
            await db.DataBase.delete_in_db(collection_str=doc["collection"], id=doc["id"])

            return JSONResponse(
                content={
                    "status": "OK",
                    "response": {"code": ITEM_DELETED_SUCCESSFULLY},
                },
                status_code=200,
            )

        # Se o item não for encontrado, retorna uma mensagem de erro
        return JSONResponse(
            content={
                "status": "ERROR",
                "response": {"code": ID_NOT_FOUND},
            },
            status_code=404,
        )

    except Exception as e:
        # Captura qualquer exceção e retorna uma mensagem de erro genérica
        raise HTTPException(status_code=500, detail=str(e))
