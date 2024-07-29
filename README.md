# FastApi + MongoDB

Este repositorio é uma base de uma api feita com **FastAPi** e usando **MongoDB** como database, visando polpar tempo na hora de desenvolvimentos de aplicações. Essa base ja contem rotas de **C.R.U.D** da database.

## Instalando

```
$ git clone https://github.com/4str0x/FastApi-Mongodb

    --> 100%

$ pip install -r requeriments.txt

    --> 100%
```

> Apos a instalação é necessario configurar as [variaveis de conexão da DataBase](https://github.com/4str0x/FastApi-Mongodb/blob/9c61b5be48b195960652109cec0cbef4a7156ad6/database/Database.py#L9)

## Rodando
Rodando localmente
```
$ uvicorn main:app --port 8080
```
Se for enviar o projeto para alguma host é necessario configurar a inicialização do servidor [no arquivo main](https://github.com/4str0x/FastApi-Mongodb/blob/9c61b5be48b195960652109cec0cbef4a7156ad6/main.py#L18)

# Rotas

## inserir dados na database (insert)
* URL - https://localhost:8080/db/insert

* Metodo HTTP - <span style="color: GREEN;">**POST**</span>

* Descrição - Inseri um objeto dentro de um coleção especificada

### Parametros de consulta
Rodando localmente
```
collection: str
payload: {"id" necessario} 
```

### Resposta
```
{
  "status": "OK",
  "response": {
    "code": "Successfully registered"
  }
}
```