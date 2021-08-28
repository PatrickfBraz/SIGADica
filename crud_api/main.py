"""
Module: Definição da API REST
Description: Modulo de definição das rotas de CRUD para o banco de dados do SIGADica
"""
import json
import logging
from os import getenv
from http import HTTPStatus
from fastapi import FastAPI, Response
from src.database_connector import MysqlHook
from src.models.response_body_models import RespostaRaiz

app = FastAPI()

mysql_hook = MysqlHook()
engine = mysql_hook.get_database_engine()

logger = logging.getLogger(__name__)

if getenv('DEBUG', 'FALSE') == 'TRUE':
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)


@app.get(
    "/",
    description="Apresentação da API",
    response_model=RespostaRaiz
)
def root_path():
    return Response(
        status_code=HTTPStatus.OK, content=json.dumps({
            "version": "0.0.1",
            "contact": "patrickfbraz@poli.ufrj.br",
            "description": """SIGADica CRUD API

            SIGADica é uma plataforma de auxilio para os estudantes da UFRJ."""
        }, default=str),
        headers={"Content-Type": "application/json"}
    )


@app.get(
    "/disciplina",
    description="Rota responsável pela busca de disciplinas",
    response_model=None
)
def bsucar_disciplinas():
    pass


@app.get(
    "/curso",
    description="Rota responsável pela busca de cursos",
    response_model=None
)
def buscar_cursos():
    pass


@app.get(
    "/curso/periodo",
    description="Rota responsável pela busca de informações de periodos de um dado curso",
    response_model=None
)
def buscar_curso_periodo():
    pass


@app.get(
    "/curso/disciplinas",
    description="Rota responsável pela busca de disciplinas de um dado curso",
    response_model=None
)
def buscar_curso_disciplinas():
    pass
