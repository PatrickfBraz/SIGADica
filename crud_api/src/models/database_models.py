from sqlalchemy import Column, Integer, String, TIMESTAMP, BOOLEAN, TEXT
from sqlalchemy.ext.declarative import declarative_base
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from datetime import datetime

Base = declarative_base()


class Curso(Base):
    __tablename__ = 'curso'
    id_curso = Column(Integer, primary_key=True)
    numero_periodos = Column(Integer)
    numero_maximo_periodos = Column(Integer)
    nome = Column(String(255))
    ano_curriculo = Column(String(255))
    situacao = Column(String(255))
    data_inclusao = Column(TIMESTAMP, default=datetime.utcnow)
    data_alteracao = Column(TIMESTAMP, default=datetime.utcnow)
    deletado = Column(BOOLEAN, default=False)


class CadastroDisciplinaCurso(Base):
    __tablename__ = 'cadastro_disciplina_curso'
    id_curso = Column(Integer, primary_key=True)
    id_disciplina = Column(Integer)
    periodo = Column(Integer)
    categoria_disciplina = Column(String)
    data_inclusao = Column(TIMESTAMP, default=datetime.utcnow)
    data_alteracao = Column(TIMESTAMP, default=datetime.utcnow)
    deletado = Column(BOOLEAN, default=False)


class Disciplina(Base):
    __tablename__ = 'disciplina'
    id_disciplina = Column(Integer, primary_key=True)
    codigo_disciplina = Column(String(6), unique=True)
    creditos = Column(Integer)
    carga_teorica = Column(Integer)
    carga_pratica = Column(Integer)
    extensao = Column(Integer)
    descricao = Column(TEXT)
    data_inclusao = Column(TIMESTAMP, default=datetime.utcnow)
    data_alteracao = Column(TIMESTAMP, default=datetime.utcnow)
    deletado = Column(BOOLEAN, default=False)


class CadastroRequisitoDisciplina(Base):
    __tablename__ = 'cadastro_requisito_disciplina'
    id_disciplina = Column(Integer, primary_key=True)
    id_disciplina_requisito = Column(Integer)
    data_inclusao = Column(TIMESTAMP, default=datetime.utcnow)
    data_alteracao = Column(TIMESTAMP, default=datetime.utcnow)
    deletado = Column(BOOLEAN, default=False)


class DisciplinasCurso(Base):
    __tablename__ = 'disciplinas_curso'
    id_curso = Column(Integer, primary_key=True)
    nome = Column(String(255))
    situacao = Column(String(255))
    curso_inativo = Column(BOOLEAN, default=True)
    codigo_disciplina = Column(String(6))
    id_disciplina = Column(Integer)
    periodo = Column(Integer)
    categoria_disciplina = Column(String(255))
    creditos = Column(Integer)
    carga_teorica = Column(Integer)
    carga_pratica = Column(Integer)
    extensao = Column(Integer)
    descricao = Column(TEXT)


class DisciplinasCursoSerializer(SQLAlchemySchema):
    class Meta:
        model = DisciplinasCurso

    id_curso = auto_field()
    nome = auto_field()
    situacao = auto_field()
    codigo_disciplina = auto_field()
    id_disciplina = auto_field()
    curso_inativo = auto_field()
    categoria_disciplina = auto_field()
    periodo = auto_field()
    creditos = auto_field()
    carga_teorica = auto_field()
    carga_pratica = auto_field()
    extensao = auto_field()
    descricao = auto_field()


class CursoSerializer(SQLAlchemySchema):
    class Meta:
        model = Curso

    id_curso = auto_field()
    numero_periodos = auto_field()
    numero_maximo_periodos = auto_field()
    nome = auto_field()
    ano_curriculo = auto_field()
    situacao = auto_field()
    data_inclusao = auto_field()
    data_alteracao = auto_field()
    deletado = auto_field()


class DisciplinaSerializer(SQLAlchemySchema):
    class Meta:
        model = Disciplina

    id_disciplina = auto_field()
    codigo_disciplina = auto_field()
    creditos = auto_field()
    carga_teorica = auto_field()
    carga_pratica = auto_field()
    extensao = auto_field()
    descricao = auto_field()
    data_inclusao = auto_field()
    data_alteracao = auto_field()
    deletado = auto_field()
