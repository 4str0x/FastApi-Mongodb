# FastApi + MongoDB
[![version : version](https://img.shields.io/badge/Version-0.1-0.svg)](https://github.com/4str0x/FastApi-Mongodb)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
-
Este repositorio é uma base de uma api feita com **FastAPi** e usando **MongoDB** como database, visando polpar tempo na hora de desenvolver aplicações 

## Instalando

```
$ git clone https://github.com/4str0x/FastApi-Mongodb

$ pip install -r requeriments.txt
```

> Apos a instalação é necessario configurar as [variaveis de conexão da DataBase]()

## Rodando
Rodando localmente
```
$ uvicorn main:app --port 8080
```
Se for enviar o projeto para alguma host é necessario configurar a inicialização do servidor [no arquivo main]()