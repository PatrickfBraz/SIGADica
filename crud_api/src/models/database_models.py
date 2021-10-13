from sqlalchemy import Column, Integer, String, TIMESTAMP, BOOLEAN, TEXT
from sqlalchemy.ext.declarative import declarative_base
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from datetime import datetime

Base = declarative_base()


class Curso(Base):
    """
    Definição de tabela
    """
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


class Usuario(Base):
    """
    Definição de tabela
    """
    __tablename__ = 'usuario'
    id_usuario = Column(Integer, primary_key=True)
    id_curso = Column(Integer)
    email = Column(String(255))
    matricula = Column(String(255))
    data_inclusao = Column(TIMESTAMP, default=datetime.utcnow)
    data_alteracao = Column(TIMESTAMP, default=datetime.utcnow)
    deletado = Column(BOOLEAN, default=False)


class CadastroDisciplinaCurso(Base):
    """
    Definição de tabela
    """
    __tablename__ = 'cadastro_disciplina_curso'
    id_curso = Column(Integer, primary_key=True)
    id_disciplina = Column(Integer)
    periodo = Column(Integer)
    categoria_disciplina = Column(String)
    data_inclusao = Column(TIMESTAMP, default=datetime.utcnow)
    data_alteracao = Column(TIMESTAMP, default=datetime.utcnow)
    deletado = Column(BOOLEAN, default=False)


class Disciplina(Base):
    """
    Definição de tabela
    """
    __tablename__ = 'disciplina'
    id_disciplina = Column(Integer, primary_key=True)
    codigo_disciplina = Column(String(6), unique=True)
    nome = Column(String(255))
    creditos = Column(Integer)
    carga_teorica = Column(Integer)
    carga_pratica = Column(Integer)
    extensao = Column(Integer)
    descricao = Column(TEXT)
    data_inclusao = Column(TIMESTAMP, default=datetime.utcnow)
    data_alteracao = Column(TIMESTAMP, default=datetime.utcnow)
    deletado = Column(BOOLEAN, default=False)


class CadastroRequisitoDisciplina(Base):
    """
    Definição de tabela
    """
    __tablename__ = 'cadastro_requisito_disciplina'
    id_disciplina = Column(Integer, primary_key=True)
    id_disciplina_requisito = Column(Integer)
    data_inclusao = Column(TIMESTAMP, default=datetime.utcnow)
    data_alteracao = Column(TIMESTAMP, default=datetime.utcnow)
    deletado = Column(BOOLEAN, default=False)


class AvaliacaoDisciplina(Base):
    """
    Definição de tabela
    """
    __tablename__ = 'avaliacao_disciplina'
    id_avaliacao = Column(Integer, primary_key=True)
    id_usuario = Column(Integer)
    id_disciplina = Column(Integer)
    nota_monitoria = Column(Integer)
    nota_dificuldade = Column(Integer)
    nota_flexibilidade = Column(Integer)
    nota_didatica = Column(Integer)
    professor = Column(String(255))
    ano_periodo = Column(String(255))
    comentario = Column(String(255))


class DisciplinaAvaliacaoMediaNotas(Base):
    """
    Definição de view
    """
    __tablename__ = 'disciplinas_avaliacao_media_notas'
    id_curso = Column(Integer)
    id_disciplina = Column(Integer, primary_key=True)
    nota_monitoria = Column(Integer)
    nota_dificuldade = Column(Integer)
    nota_flexibilidade = Column(Integer)
    nota_didatica = Column(Integer)


class DisciplinasCurso(Base):
    """
    Definição de view
    """
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


class DisciplinasAvaliacao(Base):
    """
    Definição de view
    """
    __tablename__ = 'disciplinas_avaliacao'
    id_disciplina = Column(Integer)
    id_curso = Column(Integer)
    descricao = Column(TEXT)
    id_avaliacao = Column(Integer, primary_key=True)
    data_cadastro = Column(TIMESTAMP)
    nota_monitoria = Column(Integer)
    nota_dificuldade = Column(Integer)
    nota_flexibilidade = Column(Integer)
    nota_didatica = Column(Integer)
    professor = Column(String(255))
    ano_periodo = Column(String(255))
    comentario = Column(String(255))


class DisciplinasCursoSerializer(SQLAlchemySchema):
    """
    Classe de serialização de modelo de tabela/view em json
    """

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


class DisciplinasAvaliacaoMediaNotasSerializer(SQLAlchemySchema):
    """
    Classe de serialização de modelo de tabela/view em json
    """

    class Meta:
        model = DisciplinaAvaliacaoMediaNotas

    id_curso = auto_field()
    id_disciplina = auto_field()
    nota_monitoria = auto_field()
    nota_dificuldade = auto_field()
    nota_flexibilidade = auto_field()
    nota_didatica = auto_field()


class DisciplinasAvaliacaoSerializer(SQLAlchemySchema):
    """
    Classe de serialização de modelo de tabela/view em json
    """

    class Meta:
        model = DisciplinasAvaliacao

    id_curso = auto_field()
    id_disciplina = auto_field()
    descricao = auto_field()
    id_avaliacao = auto_field()
    data_cadastro = auto_field()
    nota_monitoria = auto_field()
    nota_dificuldade = auto_field()
    nota_flexibilidade = auto_field()
    nota_didatica = auto_field()
    professor = auto_field()
    ano_periodo = auto_field()
    comentario = auto_field()


class CursoSerializer(SQLAlchemySchema):
    """
    Classe de serialização de modelo de tabela/view em json
    """

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
    """
    Classe de serialização de modelo de tabela/view em json
    """

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
