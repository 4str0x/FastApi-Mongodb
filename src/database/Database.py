import os
import motor.motor_asyncio
from dotenv import load_dotenv
from bson import ObjectId

load_dotenv()

# Chave de conexão do MongoDB mais a database da aplicação
MONGODB_CONNECTION_STRING = ""
client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_CONNECTION_STRING)
DB = client[""] # passe a database do seu projeto aqui

# Carregando as mensagens de retorno do arquivo .env
ALREADY_REGISTERED_MSG = os.getenv("ALREADY_REGISTERED_MSG")
SUCCESS_REGISTER_MSG = os.getenv("SUCCESS_REGISTER_MSG")
GENERIC_ERROR = os.getenv("GENERIC_ERROR")
ITEM_DELETED_SUCCESSFULLY = os.getenv("ITEM_DELETED_SUCCESSFULLY")
ITEM_EDITED = os.getenv("ITEM_EDITED")


def convert_object_id_to_str(obj):
    """
    Converte objetos do tipo ObjectId em suas representações de string.

    Esta função percorre recursivamente dicionários e listas para converter todas as instâncias
    de ObjectId encontradas em strings. Ignora a chave "_id" nos dicionários.

    Parameters:
        obj (Union[ObjectId, dict, list, any]): O objeto a ser convertido, que pode ser um ObjectId, um dicionário,
                                                uma lista ou qualquer outro tipo de dado.

    Returns:
        Union[str, dict, list, any]: O objeto convertido, onde todos os ObjectId foram convertidos em strings.
    """
    if isinstance(obj, ObjectId):
        return str(obj)
    elif isinstance(obj, dict):
        return {
            key: convert_object_id_to_str(value)
            for key, value in obj.items()
            if key != "_id"
        }
    elif isinstance(obj, list):
        return [convert_object_id_to_str(item) for item in obj]
    return obj


class DataBase:
    """
    Classe para gerenciar ações do banco de dados.

    Esta classe fornece métodos para: Procurar, deletar, editar, inserir e procurar todos os documentos.

    """
    
    @classmethod
    async def find_in_db(cls, collection_str: str, id: int) -> dict:
        """
        Faz uma busca em uma coleção com o filtro "id".

        Esta função percorre uma coleção especificada e busca um documento através de um id.

        Parameters:
            collection_str (str): Coleção a ser percorrida.
            id (int): Id que servirá de filtro para achar o documento especificado.

        Returns:
            dict: Documento buscado na coleção.
        """
        collection = DB[collection_str]
        Data = await collection.find_one({"id": id})
        return Data

    @classmethod
    async def insert_in_db(cls, collection_str: str, document: dict) -> str:
        """
        Insere um documento na coleção especificada.

        Esta função armazena um documento dentro de uma coleção especificada.

        Parameters:
            collection_str (str): Coleção a ser percorrida.
            document (dict): Documento que será armazenado na coleção.

        Returns:
            str: Mensagem de sucesso ou erro.
        """
        collection = DB[collection_str]
        try:
            await collection.insert_one(document)
            return SUCCESS_REGISTER_MSG
        except:
            return GENERIC_ERROR

    @classmethod
    async def delete_in_db(cls, collection_str: str, id: int) -> str:
        """
        Deleta um documento na coleção especificada.

        Esta função deleta um documento dentro de uma coleção especificada.

        Parameters:
            collection_str (str): Coleção a ser percorrida.
            id (int): Id que servirá de filtro para achar o documento especificado.

        Returns:
            str: Mensagem de sucesso ou erro.
        """
        collection = DB[collection_str]
        try:
            await collection.delete_one({"id": id})
            return ITEM_DELETED_SUCCESSFULLY
        except:
            return GENERIC_ERROR

    @classmethod
    async def edit_in_db(cls, collection_str: str, id: int, value: dict) -> str:
        """
        Edita um campo de um documento em uma coleção especificada.

        Esta função permite editar um campo de um documento em uma coleção especificada.

        Parameters:
            collection_str (str): Coleção a ser percorrida.
            id (int): Id que servirá de filtro para achar o documento especificado.
            value (dict): Campo a ser editado do documento.

        Exemplos:
            doc: {"id": 1, "Name": "fulano"}, documento existente de uma coleção.
            value: {"Name": "Claudio"}, o campo "Name" será alterado para "Claudio".

        Returns:
            str: Mensagem de sucesso ou erro.
        """
        collection = DB[collection_str]
        try:
            await collection.update_one({"id": id}, {"$set": value})
            return ITEM_EDITED
        except:
            return GENERIC_ERROR

    @classmethod
    async def find_all(cls, collection_str: str) -> list:
        """
        Faz uma busca de todos os documentos na coleção especificada.

        Esta função busca todos os documentos e retorna uma lista com os documentos buscados.

        Parameters:
            collection_str (str): Coleção a ser percorrida.

        Returns:
            list: Todos os documentos buscados na coleção.
        """
        collection = DB[collection_str]
        try:
            documents = []
            cursor = collection.find({})
            async for document in cursor:
                documents.append(convert_object_id_to_str(document))
            return documents
        except Exception as e:
            print(e)
            return []
