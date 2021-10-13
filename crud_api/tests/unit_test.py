# coding=utf-8
"""
Modulo de testes unitários da API de CRUD
"""
import json
import os, sys
from pathlib import Path

# adjust PYTHONPATH
sys.path.insert(0, str(Path(os.path.abspath('.')).parent))
sys.path.insert(0, str(Path(os.path.abspath('.')).parent.parent))

from main import app
from fastapi.testclient import TestClient
from src.models.database_models import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import logging

os.environ["CONTEX"] = "API_TEST"

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

client = TestClient(app)


class SQLiteHook:
    """
    Classe criada para definir em memória uma réplica da modelagem do banco. Assim, será possível
    realizar os testes unitários da API de CRUD
    """
    engine = create_engine('sqlite:///sigadica.db:memory:')

    def create_session(self) -> Session:
        """
        Método responsável por criar sessões no banco de dados
        Returns:
            Retorna um objeto de sessão para executar tarefas no banco de dados
        """
        return sessionmaker(self.engine)()


def test_buscar_raiz():
    logger.info("Testando rota raiz")
    response = client.get("/")
    logger.info(response.json())
    assert response.status_code == 200


def test_rotas_curso():
    logger.info("Testando criação de entidade curso")
    curso = {
        "numero_periodos": 9,
        "numero_maximo_periodos": 18,
        "nome": "teste",
        "ano_curriculo": "2020",
        "situacao": "teste"
    }
    response = client.post("/curso", data=json.dumps(curso, default=str))
    logger.info("Resposta da criação de curso: %s", response.json())
    assert response.status_code == 200
    id_curso = response.json().get('id_curso')
    response = client.get(f'/curso?id_curso={id_curso}')
    assert response.status_code == 200


def test_rotas_disciplina():
    logger.info("Testando criação de entidade disciplina")
    disciplina = {
        "codigo_disciplina": "EEL180",
        "creditos": 2,
        "carga_teorica": 2,
        "carga_pratica": 0,
        "extensao": 0,
        "descricao": "mock teste",
        "nome": "teste"
    }
    response = client.post("/disciplina", data=json.dumps(disciplina, default=str))
    logger.info("Resposta da criação de disciplina: %s", response.json())
    assert response.status_code == 200
    id_disciplina = response.json().get('id_disciplina')
    response = client.get(f'/disciplina?id_disciplina={id_disciplina}')
    assert response.status_code == 200


def test_curso_disciplina():
    logger.info("Testando criação de entidade curso")
    curso = {
        "numero_periodos": 9,
        "numero_maximo_periodos": 18,
        "nome": "teste",
        "ano_curriculo": "2020",
        "situacao": "teste"
    }
    response = client.post("/curso", data=json.dumps(curso, default=str))
    logger.info("Resposta da criação de curso: %s", response.json())
    assert response.status_code == 200
    id_curso = response.json().get('id_curso')
    response = client.get(f'/curso?id_curso:{id_curso}')
    assert response.status_code == 200
    disciplina = {
        "id_curso": id_curso,
        "nome": "teste mock",
        "codigo_disciplina": "EEL323",
        "categoria_disciplina": "obrigatoria",
        "periodo": 3,
        "creditos": 3,
        "carga_teorica": 2,
        "carga_pratica": 2,
        "extensao": 2,
        "descricao": "mock teste"
    }
    response = client.post("/curso/disciplina", data=json.dumps(disciplina, default=str))
    logger.info("Resposta da criação de curso-disciplina: %s", response.json())
    assert response.status_code == 200
    response = client.get(f'/curso/disciplinas?id_curso={id_curso}')
    logger.info("Resposta da busca de disciplinas: %s", response.json())
    assert response.status_code == 200
