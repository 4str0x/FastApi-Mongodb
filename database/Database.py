import os

import motor.motor_asyncio
from dotenv import load_dotenv
from bson import ObjectId  


load_dotenv()


# Variaveis constantes que armazena possiveis menssagens de retorno
MONGODB_CONNECTION_STRING = "mongodb+srv://astro:astro@cluster0.gkzj5ua.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
ALREADY_REGISTERED_MSG = os.getenv("ALREADY_REGISTERED_MSG")
SUCCESS_REGISTER_MSG = os.getenv("SUCCESS_REGISTER_MSG")
GENERIC_ERROR = os.getenv("GENERIC_ERROR")
ITEM_DELETED_SUCCESSFULLY = os.getenv("ITEM_DELETED_SUCCESSFULLY")


def convert_object_id_to_str(obj):
    """
    Converte objetos do tipo ObjectId em suas representações de string.
    
    Esta função percorre recursivamente dicionários e listas para converter todas as instâncias
    de ObjectId encontradas em strings. Ignorando a chave "_id" nos dicionários.

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
    Classe para gerenciar ações do banco de dados
    
    Essa classe fornece metodos para: Procurar, deletar, editar, inserir e procurar todos os documentos
    
    Attributes:
        client (MongoClient): O cliente MongoDB.
        db (Database): O banco de dados MongoDB.
    """
    
    def __init__(self) -> None:
        """
        Inicializa a instância do DatabaseHandler.
        
        Conecta ao banco de dados MongoDB usando a URI fornecida.
        """
        
        client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_CONNECTION_STRING)
        self.db = client["M_key"]
    
    
    @classmethod
    async def Find_in_db(cls, collection_str: str, id:int):
        """
        Faz uma busca em uma coleção com o filtro "id"
        
        Essa função passa pecorre uma coleção expecificada e buscar um documento atraves de um id
        
        Parameters:
            collection_str: str, Coleção a ser pecorrida
            id: int, Id que ira servir de filtro para achar o documento expecificado
        
        """
        collection = cls.db[collection_str]
        Data = await collection.find_one({"id": id})

        return Data


    @classmethod
    async def Insert_in_db(cls, collection_str: str, document: dict):
        collection = cls.db[collection_str]
        try:
            await collection.insert_one(document)
            return SUCCESS_REGISTER_MSG
        except:
            return GENERIC_ERROR


    @classmethod
    async def Deleted_in_db(cls, collection_str: str, id: int):
        collection = cls.db[collection_str]
        try:
            await collection.delete_one({"id": id})
            return ITEM_DELETED_SUCCESSFULLY
        except:
            return GENERIC_ERROR


    @classmethod
    async def Edit_in_db(cls, collection_str: str, id: int, value: dict):
        collection = cls.db[collection_str]
        try:
            await collection.update_one({"id": id}, {"$set": value})
        except:
            return GENERIC_ERROR


    @classmethod
    async def find_all(cls, collection_str: str):
        collection = cls.db[collection_str]
        try:
            documents = []
            cursor = collection.find({})
            async for document in cursor:
                documents.append(convert_object_id_to_str(document))

            return documents

        except Exception as e:
            print(e)