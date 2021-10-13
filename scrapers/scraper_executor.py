# coding=utf-8
"""
Pacote responsável pelo controle de execução do scraper dentro do ambiente container
"""
import logging
import sqlalchemy
from sqlalchemy.exc import OperationalError
from sqlalchemy.engine import Engine
from typing import NoReturn, Union
from time import sleep
from sys import exit, stdout
from os import getenv
from scraperCurso import main

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(stdout))

max_retries = 20
time_sleep = 6


def get_database_engine(user: str, password: str, host: str, port: int, db: str) -> Union[
    Engine, NoReturn]:
    """
    Função responsável por criar objeto de conexão com o banco de dados
    Args:
        user (str): Nome de usuário
        password (str): Senha
        host (str): Host do bancod e dados
        port (str): Porta de acesso
        db (str): Nome do database
    Returns:
        Objeto de conexão com o banco de dados
    """
    connection_str = 'mysql+pymysql://'
    connection_str += f'{user}:{password}@{host}:{port}/{db}'
    try:
        db_engine = sqlalchemy.create_engine(connection_str,
                                             pool_size=1,
                                             echo=False,
                                             connect_args={
                                                 'connect_timeout': 30
                                             },
                                             execution_options={
                                                 "isolation_level": "AUTOCOMMIT"
                                             }
                                             )

        return db_engine
    except OperationalError as error:
        logger.error("Não foi possivel criar engine de conexão com o banco de dados. Detalhes:")
        logger.error(error)
        return None


if __name__ == '__main__':
    logger.info("Verificando conexão com o banco de dados antes de executar o scraper")
    complete_task = False
    for tries in range(max_retries):
        engine = get_database_engine(
            user=getenv("MYSQL_DB_USER"),
            password=getenv("MYSQL_DB_PASSWORD"),
            host=getenv("MYSQL_DB_HOST"),
            port=int(getenv("MYSQL_DB_PORT")),
            db=getenv("MYSQL_DB_NAME")
        )
        try:
            if engine.connect():
                sleep(time_sleep)
                main()
                exit(0)
        except OperationalError:
            logger.info("Tentativa %s estabelecer conexão com o banco de dados" % tries)
            sleep(time_sleep)

    logger.error("Não foi possível estabelecer conexão com o banco de dados")
    exit(1)
