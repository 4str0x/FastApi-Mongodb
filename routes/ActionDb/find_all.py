import os

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

from database import Database as db  # Certifique-se de que a importação da classe está correta

# Criação do roteador para as rotas do FastAPI
router = APIRouter()
load_dotenv()  # Carrega as variáveis de ambiente do arquivo .env

# Carregando as mensagens de retorno do arquivo .env
GENERIC_ERROR = os.getenv("GENERIC_ERROR")

@router.get("/")
async def find_all(collection: str):
    """
    Busca todos os documentos de uma coleção especificada no banco de dados.

    Esta função recebe o nome de uma coleção, verifica se a coleção é permitida
    e, se for, busca todos os documentos na coleção. Se a coleção for restrita,
    retorna um erro de acesso negado. Se houver algum erro genérico, retorna uma
    mensagem de erro apropriada.

    Parameters:
        collection (str): Nome da coleção a ser buscada.

    Returns:
        JSONResponse: Resposta JSON contendo o status da operação e uma mensagem de sucesso ou erro.
    """
    try:
        # Busca todos os documentos na coleção especificada
        result = await db.DataBase.find_all(collection_str=collection)

        # Verifica se ocorreu um erro genérico
        if result == GENERIC_ERROR:
            return JSONResponse(
                content={
                    "status": "ERROR",
                    "response": {"code": GENERIC_ERROR},
                },
                status_code=500,
            )

        # Retorna os documentos encontrados
        return JSONResponse(
            content={
                "status": "OK",
                "response": result,
            },
            status_code=200,
        )
    except Exception as e:
        # Captura qualquer exceção e retorna uma mensagem de erro genérica
        raise HTTPException(status_code=500, detail=str(e))
