"""
Module: Definição da API REST
Description: Modulo de definição das rotas de CRUD para o banco de dados do SIGADica
"""
import re
import json
import logging
from os import getenv
from http import HTTPStatus
from fastapi import FastAPI, Response
from src.database_connector import MysqlHook
from src.models.response_body_models import (RespostaRaiz, RespostaBuscaDisciplina, RespostaBuscaCurso,
                                             RespostaCriacaoDisciplinaCurso, RespostaCriacaoCurso,
                                             RespostaCriacaoDisciplina,
                                             RespostaCriacaoDisciplinaRequisito, RespostaCriacaoPeriodo)
from src.models.request_body_models import (InserirCurso, InserirDisciplina, InserirDisciplinaCurso,
                                            InserirDisciplinaRequisito, InserirPeriodo)
from src.models.database_models import Disciplina, DisciplinaSerializer
from src.models.database_models import Curso, CursoSerializer
from src.models.database_models import DisciplinasCurso, DisciplinasCursoSerializer
from src.models.database_models import Periodo, Requisito
from typing import Dict, Optional


def get_api_version():
    with open('./__init__.py', 'r') as init_file:
        match = re.match(r"^__.*\"(\d\.\d\.\d)", init_file.read())
        if match:
            return match.group(1)
        else:
            return '0.0.0'


app = FastAPI(
    title="SIGADica CRUD",
    description="API de CRUD da plataforma SIGADica",
    version=get_api_version(),
)

mysql_hook = MysqlHook()
engine = mysql_hook.get_database_engine()

logger = logging.getLogger(__name__)

if getenv('DEBUG', 'FALSE') == 'TRUE':
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)


def request_response(
        json_response: Dict,
        status_code: int,
        custom_headers: Optional[Dict] = None) -> Response:
    if custom_headers:
        return Response(
            status_code=status_code,
            content=json.dumps(json_response, default=str),
            headers={"Content-Type": "application/json"}.update(custom_headers)
        )
    else:
        return Response(
            status_code=status_code,
            content=json.dumps(json_response, default=str),
            headers={"Content-Type": "application/json"}
        )


@app.get(
    "/",
    description="Apresentação da API",
    response_model=RespostaRaiz
)
def apresentacao_api():
    return request_response(
        status_code=HTTPStatus.OK,
        json_response={
            "versao": get_api_version(),
            "contato": "patrickfbraz@poli.ufrj.br",
            "descricao": """SIGADica CRUD API

            SIGADica é uma plataforma de auxilio para os estudantes da UFRJ."""
        }
    )


@app.get(
    "/disciplina",
    description="Rota responsável pela busca de disciplinas",
    response_model=RespostaBuscaDisciplina
)
def buscar_disciplinas(
        codigo_disciplina: Optional[str] = None,
        limit: Optional[int] = 10,
        creditos: Optional[int] = None
):
    session = mysql_hook.create_session()
    query = session.query(
        Disciplina.codigo_disciplina,
        Disciplina.descricao,
        Disciplina.extensao,
        Disciplina.creditos,
        Disciplina.carga_pratica,
        Disciplina.carga_teorica,
        Disciplina.data_inclusao,
        Disciplina.data_alteracao
    )
    serializer = DisciplinaSerializer()

    if creditos:
        query = query.filter(Disciplina.creditos == creditos)

    if codigo_disciplina:
        query = query.filter(Disciplina.codigo_disciplina == codigo_disciplina)

    query = query.limit(limit=limit)
    result_set = serializer.dump(query.all(), many=True)
    return request_response(json_response=result_set, status_code=HTTPStatus.OK)


@app.get(
    "/curso",
    description="Rota responsável pela busca de cursos",
    response_model=RespostaBuscaCurso
)
def buscar_cursos(
        id_curso: Optional[int] = None,
        nome: Optional[str] = None,
        situacao: Optional[str] = None,
        limit: Optional[int] = 10
):
    session = mysql_hook.create_session()
    query = session.query(
        Curso.id_curso,
        Curso.numero_periodos,
        Curso.numero_maximo_periodos,
        Curso.ano_curriculo,
        Curso.situacao,
        Curso.nome,
        Curso.data_inclusao,
        Curso.data_alteracao
    )
    serializer = CursoSerializer()

    if id_curso:
        query = query.filter(Curso.id_curso == id_curso)

    if nome:
        query = query.filter(Curso.nome.like(nome))

    if situacao:
        query.filter(Curso.situacao.like(situacao))

    query = query.limit(limit=limit)
    result_set = serializer.dump(query.all(), many=True)
    return request_response(json_response=result_set, status_code=HTTPStatus.OK)


# @app.get(
#     "/curso/periodo",
#     description="Rota responsável pela busca de informações de periodos de um dado curso",
#     response_model=None
# )
# def buscar_curso_periodo():
#     pass


@app.get(
    "/curso/disciplinas",
    description="Rota responsável pela busca de disciplinas de um dado curso",
    response_model=None
)
def buscar_curso_disciplinas(
        id_curso: Optional[int] = None,
        situacao: Optional[str] = None,
        nome: Optional[str] = None,
        ativo: Optional[int] = 0
):
    session = mysql_hook.create_session()
    query = session.query(
        DisciplinasCurso.id_curso,
        DisciplinasCurso.codigo_disciplina,
        DisciplinasCurso.situacao,
        DisciplinasCurso.nome,
        DisciplinasCurso.creditos,
        DisciplinasCurso.carga_teorica,
        DisciplinasCurso.carga_pratica,
        DisciplinasCurso.extensao,
        DisciplinasCurso.descricao,
        DisciplinasCurso.ativo,
        DisciplinasCurso.periodo
    )
    serializer = DisciplinasCursoSerializer()

    if not id_curso and not nome:
        return request_response(
            json_response={
                "error": "É necessário informar pelo menos um filtro de curso (nome ou ID)"
            },
            status_code=HTTPStatus.BAD_REQUEST
        )

    if id_curso:
        query = query.filter(DisciplinasCurso.id_curso == id_curso)

    if nome:
        query = query.filter(DisciplinasCurso.nome.like(nome))

    if situacao:
        query.filter(DisciplinasCurso.situacao.like(situacao))

    # query = query.filter(DisciplinasCurso.ativo is True)

    print(query)

    result_set = serializer.dump(query.all(), many=True)
    return request_response(json_response=result_set, status_code=HTTPStatus.OK)


@app.post(
    "/curso/disciplina",
    description="Rota responsável pela criação de uma disciplina associada a um curso",
    response_model=RespostaCriacaoDisciplinaCurso
)
def criar_disciplina_associada_curso(request_body: InserirDisciplinaCurso):
    session = mysql_hook.create_session()
    try:
        disciplina = Disciplina(
            codigo_disciplina=request_body.codigo_disciplina,
            creditos=request_body.creditos,
            carga_teorica=request_body.carga_teorica,
            carga_pratica=request_body.carga_pratica,
            extensao=request_body.extensao,
            descricao=request_body.descricao,
        )
        session.add(disciplina)
        session.commit()
        periodo = Periodo(
            id_curso=request_body.id_curso,
            codigo_disciplina=request_body.codigo_disciplina,
            ativo=1,
            periodo=request_body.periodo,
        )
        session.add(periodo)
        session.commit()
        return request_response(
            json_response={
                "mensagem": "Objetos inseridos com sucesso!"
            },
            status_code=HTTPStatus.OK
        )
    except Exception as error:
        return request_response(
            json_response={
                "mensagem": "Erro na criação das entidades: %s" % error
            },
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR
        )


@app.post(
    "/curso",
    description="Rota responsável pela criação de entidade curso",
    response_model=RespostaCriacaoCurso
)
def criar_curso(request_body: InserirCurso):
    session = mysql_hook.create_session()
    try:
        curso = Curso(
            numero_periodos=request_body.numero_periodos,
            numero_maximo_periodos=request_body.numero_maximo_periodos,
            nome=request_body.nome,
            ano_curriculo=request_body.ano_curriculo,
            situacao=request_body.situacao,
        )
        session.add(curso)
        session.commit()
        session.refresh(curso)
        serializer = CursoSerializer()
        return request_response(
            json_response=serializer.dump(curso),
            status_code=HTTPStatus.OK
        )
    except Exception as error:
        return request_response(
            json_response={
                "mensagem": "Erro na criação do curso: %s" % error
            },
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR
        )


@app.post(
    "/disciplina",
    description="Rota responsável pela criação de entidade disciplina",
    response_model=RespostaCriacaoDisciplina
)
def criar_disciplina(request_body: InserirDisciplina):
    session = mysql_hook.create_session()
    try:
        disciplina = Disciplina(
            codigo_disciplina=request_body.codigo_disciplina,
            creditos=request_body.creditos,
            carga_teorica=request_body.carga_teorica,
            carga_pratica=request_body.carga_pratica,
            extensao=request_body.extensao,
            descricao=request_body.descricao,
        )
        session.add(disciplina)
        session.commit()
        session.refresh(disciplina)
        serializer = DisciplinaSerializer()

        return request_response(
            json_response=serializer.dump(disciplina),
            status_code=HTTPStatus.OK
        )

    except Exception as error:
        return request_response(
            json_response={
                "mensagem": "Erro na criação da disciplina: %s" % error
            },
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR
        )


@app.post(
    "/disciplina/requisito",
    description="Rota responsável pela criação de entidade requisito",
    response_model=RespostaCriacaoDisciplinaRequisito
)
def criar_requisito_disciplina(request_body: InserirDisciplinaRequisito):
    session = mysql_hook.create_session()
    try:
        requisito = Requisito(
            codigo_disciplina=request_body.codigo_disciplina,
            codigo_disciplina_requisito=request_body.codigo_disciplina_requisito
        )
        session.add(requisito)
        session.commit()
        session.refresh(requisito)
        return request_response(
            json_response={
                "mensagem": "Objeto criado com sucesso!"
            },
            status_code=HTTPStatus.OK
        )
    except Exception as error:
        return request_response(
            json_response={
                "mensagem": "Erro na criação do requisito: %s" % error
            },
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR
        )


@app.post(
    "/curso/periodo",
    description="Rota responsável pela criação de entidade periodo",
    response_model=RespostaCriacaoPeriodo
)
def criar_requisito_disciplina(request_body: InserirPeriodo):
    session = mysql_hook.create_session()
    try:
        periodo = Periodo(
            id_curso=request_body.id_curso,
            codigo_disciplina=request_body.codigo_disciplina,
            periodo=request_body.periodo,
            ativo=1
        )
        session.add(periodo)
        session.commit()
        session.refresh(periodo)
        return request_response(
            json_response={
                "mensagem": "Objeto criado com sucesso!"
            },
            status_code=HTTPStatus.OK
        )
    except Exception as error:
        return request_response(
            json_response={
                "mensagem": "Erro na criação do periodo: %s" % error
            },
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR
        )
