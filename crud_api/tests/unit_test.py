# coding=utf-8
"""
..
"""
import os, sys
from pathlib import Path

sys.path.insert(0, str(Path(os.path.abspath('.')).parent))
from main import app
from fastapi.testclient import TestClient
from src.models.database_models import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

client = TestClient(app)


class SQLiteHook:
    engine = create_engine('sqlite:///:memory:')

    def create_session(self):
        return sessionmaker(self.engine)()


mysql_hook = SQLiteHook()
session = mysql_hook.create_session()

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200

# def test_criar_curso():
#     pass
#
#
# def test_buscar_cursos():
#     pass
#
#
# def test_criar_disciplina():
#     pass
#
#
# def test_buscar_disciplinas():
#     pass
#
#
# def test_criar_requisito_disciplina():
#     pass
#
#
# def test_criar_cadastro_disciplina_curso():
#     pass
#
#
# def test_criar_disciplina_associada_curso():
#     pass
#
#
# def test_buscar_curso_disciplinas():
#     pass
