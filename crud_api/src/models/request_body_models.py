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

class InserirPeriodo(BaseModel):
    """
    Corpo esperado pela chamada de criação de entidade periodo
    """
    id_curso: int
    codigo_disciplina: str
    periodo: int


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
            raise ValueError('Código da disciplina deve ser compsoto por 3 caracteres e 3 digitos. Ex: MMA123')
        return value


class InserirDisciplinaCurso(BaseModel):
    """
    Corpo esperado pela chamada de criação da relação entre a entidade curso e entidade disciplina por intermédio do
    periodo
    """
    id_curso: int
    codigo_disciplina: str
    periodo: int
    creditos: int
    carga_teorica: Optional[int]
    carga_pratica: Optional[int]
    extensao: Optional[int]
    descricao: Optional[str]

    @validator('codigo_disciplina')
    def codigo_disciplina_must_have_6_digits(cls, value):
        if len(value) != 6:
            raise ValueError('Código da disciplina deve ser compsoto por 3 caracteres e 3 digitos. Ex: MMA123')
        return value


class InserirDisciplinaRequisito(BaseModel):
    """
    Corpo esperado pela chamada de criação de entidade requisito
    """
    codigo_disciplina: str
    codigo_disciplina_requisito: str

    @validator('codigo_disciplina')
    def codigo_disciplina_must_have_6_digits(cls, value):
        if len(value) != 6:
            raise ValueError('Código da disciplina deve ser compsoto por 3 caracteres e 3 digitos. Ex: MMA123')
        return value

    @validator('codigo_disciplina_requisito')
    def codigo_disciplina_requisito_must_have_6_digits(cls, value):
        if len(value) != 6:
            raise ValueError('Código da disciplina deve ser compsoto por 3 caracteres e 3 digitos. Ex: MMA123')
        return value
