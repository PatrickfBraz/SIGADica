from sqlalchemy import Column, Integer, String, TIMESTAMP, BOOLEAN, TEXT
from sqlalchemy.ext.declarative import declarative_base
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field

Base = declarative_base()


class Curso(Base):
    __tablename__ = 'curso'
    id_curso = Column(Integer, primary_key=True)
    numero_periodos = Column(Integer)
    numero_maximo_periodos = Column(Integer)
    nome = Column(String(255))
    ano_curriculo = Column(String(255))
    situacao = Column(String(255))
    data_inclusao = Column(TIMESTAMP)
    data_alteracao = Column(TIMESTAMP)


class Periodo(Base):
    __tablename__ = 'periodo'
    id_curso = Column(Integer, primary_key=True)
    codigo_disciplina = Column(String(6))
    ativo = Column(BOOLEAN)
    periodo = Column(Integer)
    data_inclusao = Column(TIMESTAMP)
    data_alteracao = Column(TIMESTAMP)


class Disciplina(Base):
    __tablename__ = 'disciplina'
    codigo_disciplina = Column(String(6), primary_key=True)
    creditos = Column(Integer)
    carga_teorica = Column(Integer)
    carga_pratica = Column(Integer)
    extensao = Column(Integer)
    descricao = Column(TEXT)
    data_inclusao = Column(TIMESTAMP)
    data_alteracao = Column(TIMESTAMP)


class Requisito(Base):
    __tablename__ = 'requisito'
    codigo_disciplina = Column(String(6), primary_key=True)
    codigo_disciplina_requisito = Column(String(6))
    data_inclusao = Column(TIMESTAMP)
    data_alteracao = Column(TIMESTAMP)


class DisciplinasCurso(Base):
    __tablename__ = 'disciplinas_curso'
    id_curso = Column(Integer, primary_key=True)
    nome = Column(String(255))
    situacao = Column(String(255))
    codigo_disciplina = Column(String(6))
    ativo = Column(BOOLEAN)
    periodo = Column(Integer)
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
    ativo = auto_field()
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


class DisciplinaSerializer(SQLAlchemySchema):
    class Meta:
        model = Disciplina

    codigo_disciplina = auto_field()
    creditos = auto_field()
    carga_teorica = auto_field()
    carga_pratica = auto_field()
    extensao = auto_field()
    descricao = auto_field()
    data_inclusao = auto_field()
    data_alteracao = auto_field()
