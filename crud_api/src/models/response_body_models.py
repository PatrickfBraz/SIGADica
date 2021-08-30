from pydantic import BaseModel
from typing import Optional, List


class RespostaRaiz(BaseModel):
    """
    Resposta retornada pelo caminho raiz da API
    """
    versao: str
    contato: str
    descricao: str


class RespostaCriacaoCurso(BaseModel):
    """
    Corpo esperado pela chamada de criação de entidade curso
    """
    id_curso: int
    numero_periodos: Optional[int]
    numero_maximo_periodos: Optional[int]
    nome: str
    ano_curriculo: Optional[str]
    situacao: str
    data_inclusao: str
    data_alteracao: str


class RespostaBuscaCurso(BaseModel):
    """
    Corpo esperado pela chamada de criação de entidade curso
    """
    cursos: List[RespostaCriacaoCurso]


class RespostaCriacaoDisciplina(BaseModel):
    """
    Corpo esperado pela chamada de criação de entidade disciplina
    """
    codigo_disciplina: str
    creditos: int
    carga_teorica: Optional[int]
    carga_pratica: Optional[int]
    extensao: Optional[int]
    descricao: Optional[str]
    data_inclusao: str
    data_alteracao: str


class RespostaBuscaDisciplina(BaseModel):
    """
    Corpo esperado pela chamada de criação de entidade disciplina
    """
    disciplinas: List[RespostaCriacaoDisciplina]
    mensagem: str


class RespostaCriacaoDisciplinaCurso(BaseModel):
    """
    Corpo esperado pela chamada de criação da relação entre a entidade curso e entidade disciplina por intermédio do
    periodo
    """
    mensagem: str


class RespostaCriacaoDisciplinaRequisito(BaseModel):
    """
    Corpo esperado pela chamada de criação de entidade requisito
    """
    mensagem: str


class RespostaCriacaoPeriodo(BaseModel):
    """
    Corpo esperado pela chamada de criação de entidade requisito
    """
    mensagem: str
