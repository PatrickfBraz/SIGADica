from pydantic import BaseModel, validator
from typing import Optional


class InserirCurso(BaseModel):
    """
    Corpo esperado pela chamada de criação de entidade curso
    """
    numero_periodos: Optional[int]
    numero_maximo_periodos: Optional[int]
    nome: str
    ano_curriculo: Optional[str]
    situacao: str


class InserirCadastroDisciplinaCurso(BaseModel):
    """
    Corpo esperado pela chamada de criação de entidade periodo
    """
    id_curso: int
    id_disciplina: str
    periodo: int
    categoria_disciplina: str


class InserirDisciplina(BaseModel):
    """
    Corpo esperado pela chamada de criação de entidade disciplina
    """
    codigo_disciplina: str
    creditos: int
    carga_teorica: Optional[int]
    carga_pratica: Optional[int]
    extensao: Optional[int]
    descricao: Optional[str]

    @validator('codigo_disciplina')
    def codigo_disciplina_must_have_6_digits(cls, value):
        if len(value) != 6:
            raise ValueError(
                'Código da disciplina deve ser compsoto por 3 caracteres e 3 digitos. Ex: MMA123')
        return value


class InserirDisciplinaCurso(BaseModel):
    """
    Corpo esperado pela chamada de criação da relação entre a entidade curso e entidade disciplina por intermédio do
    periodo
    """
    id_curso: int
    codigo_disciplina: str
    categoria_disciplina: Optional[str] = 'obrigatoria'
    periodo: Optional[int] = None
    creditos: int
    carga_teorica: Optional[int] = None
    carga_pratica: Optional[int] = None
    extensao: Optional[int] = None
    descricao: Optional[str] = None

    @validator('codigo_disciplina')
    def codigo_disciplina_must_have_6_digits(cls, value):
        if len(value) != 6:
            raise ValueError(
                'Código da disciplina deve ser compsoto por 3 caracteres e 3 digitos. Ex: MMA123')
        return value


class InserirCadastroRequisitoDisciplina(BaseModel):
    """
    Corpo esperado pela chamada de criação de entidade requisito
    """
    codigo_disciplina: Optional[str] = None
    codigo_disciplina_requisito: Optional[str] = None
    id_disciplina: Optional[int] = None
    id_disciplina_requisito: Optional[int] = None

    @validator('codigo_disciplina')
    def codigo_disciplina_must_have_6_digits(cls, value):
        if len(value) != 6:
            raise ValueError(
                'Código da disciplina deve ser compsoto por 3 caracteres e 3 digitos. Ex: MMA123')
        return value

    @validator('codigo_disciplina_requisito')
    def codigo_disciplina_requisito_must_have_6_digits(cls, value):
        if len(value) != 6:
            raise ValueError(
                'Código da disciplina deve ser compsoto por 3 caracteres e 3 digitos. Ex: MMA123')
        return value


class CadastrarUsuario(BaseModel):
    """
    Corpo esperado pela chamada de criação de entidade usuario
    """
    matricula: str
    email: str
    id_curso: int
    id_usuario: int


class CadastrarAvaliacaoDisciplina(BaseModel):
    """
    Corpo esperado pela chamada de criação de entidade disciplina_avaliacao
    """
    id_usuario: int
    id_disciplina: int
    nota_monitoria: int
    nota_dificuldade: int
    nota_flexibilidade: int
    nota_didatica: int
    professor: Optional[str]
    ano_periodo: Optional[str]
    comentario: Optional[str]
