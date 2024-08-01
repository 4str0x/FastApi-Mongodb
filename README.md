# FastApi + MongoDB

Este repositório é uma base de uma API feita com **FastAPI** e usando **MongoDB** como banco de dados, visando poupar tempo no desenvolvimento de aplicações. Esta base já contém rotas de **C.R.U.D** para o banco de dados.

## Instalando

```sh
$ git clone https://github.com/4str0x/FastApi-Mongodb

    --> 100%

$ pip install -r requirements.txt

    --> 100%
```

> Após a instalação, é necessário configurar as [variáveis de conexão do banco de dados](https://github.com/4str0x/FastApi-Mongodb/blob/main/src%2Fdatabase%2FDatabase.py#L9).

## Rodando

Rodando localmente:
```sh
$ uvicorn main:app --port 8080
```

Se for enviar o projeto para alguma host, é necessário configurar a inicialização do servidor [no arquivo main](https://github.com/4str0x/FastApi-Mongodb/blob/9c61b5be48b195960652109cec0cbef4a7156ad6/main.py#L18).

# Rotas

## Inserir dados no banco de dados (insert)
* **URL** - https://localhost:8080/db/insert/
* **Método HTTP** - **POST**
* **Descrição** - Insere um objeto dentro de uma coleção especificada.

### Parâmetros de consulta
```json
{
  "collection": "string",
  "payload": {
    "id": "necessário"
  }
}
```

### Resposta
```json
{
  "status": "OK",
  "response": {
    "code": "Successfully registered"
  }
}
```

## Procurar um documento (find_one)
* **URL** - https://localhost:8080/db/find/
* **Método HTTP** - **POST**
* **Descrição** - Esta rota procura um documento específico dentro de uma coleção especificada.

### Parâmetros de consulta
```json
{
  "id": "int",
  "collection": "string"
}
```

### Resposta
```json
{
  "status": "OK",
  "response": {
    "id": 4,
    "Nome": "Test_Ronald Farrell"
  }
}
```

## Deletar um documento (delete)
* **URL** - https://localhost:8080/db/delete/
* **Método HTTP** - **POST**
* **Descrição** - Deleta um documento dentro de uma coleção.

### Parâmetros de consulta
```json
{
  "id": "int",
  "collection": "string"
}
```

### Resposta
```json
{
  "status": "OK",
  "response": {
    "code": "Item deleted successfully"
  }
}
```

## Editar um campo em um documento (edit)
* **URL** - https://localhost:8080/db/edit/
* **Método HTTP** - **POST**
* **Descrição** - Edita um campo específico de um documento.

### Parâmetros de consulta
```json
{
  "id": "int",
  "collection": "string",
  "value": "dict {}"
}
```

### Resposta
```json
{
  "status": "OK",
  "response": {
    "code": "Item edited successfully"
  }
}
```

## Procurar todos os documentos dentro de uma coleção (find_all)
* **URL** - https://localhost:8080/db/find/all/{collection}
* **Método HTTP** - **GET**
* **Descrição** - Esta rota retorna todos os documentos de uma coleção especificada.

### Exemplo de uso
```sh
https://localhost:8080/db/find/all/users
```

### Resposta
```json
{
  "status": "OK",
  "response": {
    "documents": []
  }
}
```