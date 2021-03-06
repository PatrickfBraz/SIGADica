"""
Module: Definição da API REST
Description: Modulo de definição das rotas de CRUD para o banco de dados do SIGADica
"""
import re
import json
import logging
from os import getenv
from http import HTTPStatus
from fastapi import FastAPI, Response, Depends
from src.database_connector import MysqlHook
from src.models.response_body_models import (RespostaRaiz, RespostaBuscaDisciplina,
                                             RespostaBuscaCurso,
                                             RespostaCriacaoDisciplinaCurso, RespostaCriacaoCurso,
                                             RespostaCriacaoDisciplina,
                                             RespostaBuscaDisciplinaCurso,
                                             RespostaCriacaoDisciplinaRequisito,
                                             RespostaCriacaoPeriodo,
                                             RespostaCriacaoUsuario,
                                             RespostaBuscaDisciplinasAvaliacao,
                                             RespostaBuscaDisciplinaAvaliacaoMediaNotas)
from src.models.request_body_models import (InserirCurso, InserirDisciplina, InserirDisciplinaCurso,
                                            InserirCadastroRequisitoDisciplina,
                                            InserirCadastroDisciplinaCurso, CadastrarUsuario,
                                            CadastrarAvaliacaoDisciplina)
from src.models.database_models import Disciplina, DisciplinaSerializer
from src.models.database_models import Curso, CursoSerializer
from src.models.database_models import DisciplinasCurso, DisciplinasCursoSerializer
from src.models.database_models import CadastroDisciplinaCurso, CadastroRequisitoDisciplina
from src.models.database_models import Usuario, AvaliacaoDisciplina
from src.models.database_models import DisciplinasAvaliacao, DisciplinasAvaliacaoSerializer
from src.models.database_models import (DisciplinaAvaliacaoMediaNotas,
                                        DisciplinasAvaliacaoMediaNotasSerializer)
from typing import Dict, Optional
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
from src.models.database_models import Base as DatabaseBaseModels


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

hook = MysqlHook()
mysql_session = hook.create_session()

logger = logging.getLogger(__name__)

if getenv('DEBUG', 'FALSE') == 'TRUE':
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)


# Dependency
def get_database_session():
    if getenv("CONTEX", "CONTAINER").upper() == "API_TEST":
        engine = create_engine('sqlite:///sigadica.db:memory:',
                               connect_args={"check_same_thread": False})
        DatabaseBaseModels.metadata.create_all(engine)
        session = sessionmaker(engine)()
        try:
            yield session
        except Exception as error:
            logger.exception(error)
    else:
        engine = hook.get_database_engine()
        session = mysql_session(bind=engine.connect())
        try:
            yield session
        except Exception as error:
            logger.exception(error)


# response utils
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
        id_disciplina: Optional[int] = None,
        limit: Optional[int] = 10,
        deletado: Optional[int] = 0,
        creditos: Optional[int] = None,
        session: Session = Depends(get_database_session)
):
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

    if id_disciplina:
        query = query.filter(Disciplina.id_disciplina == id_disciplina)

    query = query.filter(Disciplina.deletado == deletado)
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
        deletado: Optional[int] = 0,
        limit: Optional[int] = 10,
        session: Session = Depends(get_database_session)
):
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

    query = query.filter(Curso.deletado == deletado)

    query = query.limit(limit=limit)
    result_set = serializer.dump(query.all(), many=True)
    return request_response(json_response=result_set, status_code=HTTPStatus.OK)


@app.get(
    "/curso/disciplinas",
    description="Rota responsável pela busca de disciplinas de um dado curso",
    response_model=RespostaBuscaDisciplinaCurso
)
def buscar_curso_disciplinas(
        id_curso: Optional[int] = None,
        situacao: Optional[str] = None,
        nome: Optional[str] = None,
        inativo: Optional[int] = 0,
        categoria: Optional[str] = None,
        session: Session = Depends(get_database_session)
):
    query = session.query(
        DisciplinasCurso.id_curso,
        DisciplinasCurso.id_disciplina,
        DisciplinasCurso.codigo_disciplina,
        DisciplinasCurso.situacao,
        DisciplinasCurso.nome,
        DisciplinasCurso.creditos,
        DisciplinasCurso.carga_teorica,
        DisciplinasCurso.carga_pratica,
        DisciplinasCurso.extensao,
        DisciplinasCurso.descricao,
        DisciplinasCurso.curso_inativo,
        DisciplinasCurso.periodo,
        DisciplinasCurso.categoria_disciplina
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
        query = query.filter(DisciplinasCurso.situacao.like(situacao))

    if categoria:
        query = query.filter(DisciplinasCurso.categoria_disciplina.like(categoria))

    query = query.filter(DisciplinasCurso.curso_inativo == bool(inativo))

    result_set = serializer.dump(query.all(), many=True)
    return request_response(json_response=result_set, status_code=HTTPStatus.OK)


@app.post(
    "/curso/disciplina",
    description="Rota responsável pela criação de uma disciplina associada a um curso",
    response_model=RespostaCriacaoDisciplinaCurso
)
def criar_disciplina_associada_curso(request_body: InserirDisciplinaCurso,
                                     session: Session = Depends(get_database_session)):
    try:
        disciplina = Disciplina(
            codigo_disciplina=request_body.codigo_disciplina,
            creditos=request_body.creditos,
            carga_teorica=request_body.carga_teorica,
            carga_pratica=request_body.carga_pratica,
            extensao=request_body.extensao,
            descricao=request_body.descricao,
            nome=request_body.nome
        )
        session.add(disciplina)
        session.commit()
        session.refresh(disciplina)
        periodo = CadastroDisciplinaCurso(
            id_curso=request_body.id_curso,
            id_disciplina=disciplina.id_disciplina,
            periodo=request_body.periodo,
            categoria_disciplina=request_body.categoria_disciplina
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
def criar_curso(request_body: InserirCurso, session: Session = Depends(get_database_session)):
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
def criar_disciplina(request_body: InserirDisciplina,
                     session: Session = Depends(get_database_session)):
    try:
        disciplina = Disciplina(
            codigo_disciplina=request_body.codigo_disciplina,
            creditos=request_body.creditos,
            carga_teorica=request_body.carga_teorica,
            carga_pratica=request_body.carga_pratica,
            extensao=request_body.extensao,
            descricao=request_body.descricao,
            nome=request_body.nome
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
def criar_requisito_disciplina(request_body: InserirCadastroRequisitoDisciplina,
                               session: Session = Depends(get_database_session)):
    try:
        id_disciplina = request_body.id_disciplina
        id_disciplina_requisito = request_body.id_disciplina_requisito
        if not id_disciplina:
            if not request_body.codigo_disciplina:
                return request_response(
                    json_response={"messagem": "Nem o código nem o id da disciplina foi informado"},
                    status_code=HTTPStatus.BAD_REQUEST
                )
            verify = session.query(Disciplina.id_disciplina).filter(
                Disciplina.codigo_disciplina == request_body.codigo_disciplina).first()
            if not verify:
                return request_response(
                    json_response={"messagem": "Código da disciplina %s não encontrado" %
                                               request_body.codigo_disciplina},
                    status_code=HTTPStatus.BAD_REQUEST
                )
            else:
                id_disciplina = verify.id_disciplina

        if not id_disciplina_requisito:
            if not request_body.codigo_disciplina_requisito:
                return request_response(
                    json_response={
                        "messagem": "Nem o código nem o id da disciplina requisito foi informado"},
                    status_code=HTTPStatus.BAD_REQUEST
                )
            verify = session.query(Disciplina.id_disciplina).filter(
                Disciplina.codigo_disciplina == request_body.codigo_disciplina_requisito).first()
            if not verify:
                return request_response(
                    json_response={"messagem": "Código da disciplina requisito %s não encontrado" %
                                               request_body.codigo_disciplina_requisito},
                    status_code=HTTPStatus.BAD_REQUEST
                )
            else:
                id_disciplina_requisito = verify.id_disciplina

        requisito = CadastroRequisitoDisciplina(
            id_disciplina=id_disciplina,
            id_disciplina_requisito=id_disciplina_requisito
        )
        session.add(requisito)
        session.commit()
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
def criar_cadastro_disciplina_curso(request_body: InserirCadastroDisciplinaCurso,
                                    session: Session = Depends(get_database_session)):
    try:
        periodo = CadastroDisciplinaCurso(
            id_curso=request_body.id_curso,
            id_disciplina=request_body.id_disciplina,
            periodo=request_body.periodo,
            categoria_disciplina=request_body.categoria_disciplina
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


@app.post(
    "/usuario",
    description="Rota responsável pela criação de entidade usuário",
    response_model=RespostaCriacaoUsuario
)
def cadastrar_usuario(request_body: CadastrarUsuario,
                      session: Session = Depends(get_database_session)):
    """
    Rota responsável pelo cadastro de usuarios
    Args:
        request_body (CadastrarUsuario): Corpo json esperado pela requisição

    Returns:
        Uma mensagem de aviso caso tenha ocorrido sucesso ou falha
    """

    try:
        usuario = Usuario(
            id_usuario=request_body.id_usuario,
            id_curso=request_body.id_curso,
            email=request_body.email,
            matricula=request_body.matricula
        )
        session.add(usuario)
        session.commit()
        session.refresh(usuario)

        return request_response(
            json_response={
                "mensagem": "Usuário cadastrado com sucesso!"
            },
            status_code=HTTPStatus.OK
        )

    except Exception as error:
        return request_response(
            json_response={
                "mensagem": "Erro na criação do usuário: %s" % error
            },
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR
        )


@app.post(
    "/disciplina/avaliacao",
    description="Rota responsável pela criação de avaliação de disciplina",
    response_model=RespostaCriacaoPeriodo
)
def cadastrar_avaliacao(request_body: CadastrarAvaliacaoDisciplina,
                        session: Session = Depends(get_database_session)):
    """
    Rota responsável pelo cadastro de avaliações de disciplinas
    Args:
        request_body (CadastrarAvaliacaoDisciplina): Objeto json esperado no corpo da requisição

    Returns:
        uma mensagem de aviso caso tenha dado sucesso ou falha
    """

    try:
        avaliacao = AvaliacaoDisciplina(
            id_usuario=request_body.id_usuario,
            id_disciplina=request_body.id_disciplina,
            nota_monitoria=request_body.nota_monitoria,
            nota_dificuldade=request_body.nota_dificuldade,
            nota_flexibilidade=request_body.nota_flexibilidade,
            nota_didatica=request_body.nota_didatica,
            professor=request_body.professor,
            ano_periodo=request_body.ano_periodo,
            comentario=request_body.comentario,
        )
        session.add(avaliacao)
        session.commit()
        session.refresh(avaliacao)

        return request_response(
            json_response={
                "mensagem": "Avaliação de disciplina cadastrada com sucesso!"
            },
            status_code=HTTPStatus.OK
        )

    except Exception as error:
        return request_response(
            json_response={
                "mensagem": "Erro no cadastro de avaliação: %s" % error
            },
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR
        )


@app.get(
    "/disciplina/avaliacao",
    description="Rota responsável pela bsuca de disciplinas e suas avaliações",
    response_model=RespostaBuscaDisciplinasAvaliacao
)
def buscar_avaliacoes_disciplinas(
        id_curso: int,
        id_disciplina: Optional[int],
        limit: Optional[int] = 1000,
        session: Session = Depends(get_database_session)
):
    """
    Rota responsável pela busca de avaliações de disciplinas
    Args:
        id_curso (int): id do curso
        id_disciplina (int): id da disciplina
        limit (int):  limite de elementos que devem ser retornados

    Returns:
        Retorna um JSON ARRAY com as informações buscadas
    """
    try:

        query = session.query(
            DisciplinasAvaliacao.id_disciplina,
            DisciplinasAvaliacao.descricao,
            DisciplinasAvaliacao.id_avaliacao,
            DisciplinasAvaliacao.data_cadastro,
            DisciplinasAvaliacao.nota_didatica,
            DisciplinasAvaliacao.nota_dificuldade,
            DisciplinasAvaliacao.nota_flexibilidade,
            DisciplinasAvaliacao.nota_monitoria,
            DisciplinasAvaliacao.professor,
            DisciplinasAvaliacao.ano_periodo,
            DisciplinasAvaliacao.comentario
        )
        serializer = DisciplinasAvaliacaoSerializer()

        if not id_curso:
            return request_response(
                json_response={
                    "error": "É necessário informar o ID do curso para realizar a busca"
                },
                status_code=HTTPStatus.BAD_REQUEST
            )

        query = query.filter(DisciplinasAvaliacao.id_curso == id_curso)

        if id_disciplina:
            query = query.filter(DisciplinasAvaliacao.id_disciplina == id_disciplina)

        query = query.limit(limit=limit)

        result_set = serializer.dump(query.all(), many=True)
        return request_response(json_response=result_set, status_code=HTTPStatus.OK)
    except Exception as error:
        return request_response(
            json_response={
                "error": "Ocorreu um erro ao buscar as avaliações de disciplinas: %s" % error
            },
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR
        )


@app.get(
    "/disciplina/avaliacao/notas",
    description="Rota responsável pela bsuca da média de notas de uma avaliação",
    response_model=RespostaBuscaDisciplinaAvaliacaoMediaNotas
)
def buscar_notas_medias_avaliacoes_disciplinas(
        id_curso: int,
        id_disciplina: int,
        limit: Optional[int] = 1000,
        session: Session = Depends(get_database_session)
):
    """
    Rota responsável pela bsuca da média de notas de uma avaliação
    Args:
        id_curso (int): id do curso
        id_disciplina (int): id da disciplina
        limit (int):  limite de elementos que devem ser retornados

    Returns:
        Retorna um JSON com as informações buscadas para a dada disciplina
    """
    try:

        query = session.query(
            DisciplinaAvaliacaoMediaNotas.id_disciplina,
            DisciplinaAvaliacaoMediaNotas.id_curso,
            DisciplinaAvaliacaoMediaNotas.nota_didatica,
            DisciplinaAvaliacaoMediaNotas.nota_dificuldade,
            DisciplinaAvaliacaoMediaNotas.nota_monitoria,
            DisciplinaAvaliacaoMediaNotas.nota_flexibilidade
        )
        serializer = DisciplinasAvaliacaoMediaNotasSerializer()

        if not id_curso or not id_disciplina:
            return request_response(
                json_response={
                    "error": "É necessário informar o ID do curso e disciplina para realizar a busca"
                },
                status_code=HTTPStatus.BAD_REQUEST
            )

        query = query.filter(DisciplinaAvaliacaoMediaNotas.id_curso == id_curso)
        query = query.filter(DisciplinaAvaliacaoMediaNotas.id_disciplina == id_disciplina)

        query = query.limit(limit=limit)

        result_set = serializer.dump(query.first(), many=False)
        return request_response(json_response=result_set, status_code=HTTPStatus.OK)
    except Exception as error:
        return request_response(
            json_response={
                "error": "Ocorreu um erro ao buscar as notas das "
                         "avaliações de disciplinas: %s" % error
            },
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR
        )
