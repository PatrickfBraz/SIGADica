import logging
import sqlalchemy
from sqlalchemy.exc import OperationalError
from sqlalchemy.engine import Engine
from typing import NoReturn, Union
from time import sleep
from sys import exit, stdout
from os import getenv

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(stdout))

max_retries = 6
time_sleep = 5


def get_database_engine(user, password, host, port, db) -> Union[Engine, NoReturn]:
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


def setup_database(engine: Engine):
    try:
        logger.info("Executando querys de configuração")
        with open('querys/set_up_querys.sql') as query_file:
            querys = query_file.read()
        querys = querys.split('---s20soidk2du298d---')
        with engine.connect() as conn:
            for query in querys:
                logger.info("Executando query: %s" % query)
                conn.execute(query)
        return True
    except Exception as error:
        logger.error("Erro ao executar configuração do banco: %s" % error)
        return False


if __name__ == '__main__':
    logger.info("Iniciando setup do banco de dados")
    complete_task = False
    for tries in range(max_retries):
        engine = get_database_engine(
            user=getenv("MYSQL_DB_USER"),
            password=getenv("MYSQL_DB_PASSWORD"),
            host=getenv("MYSQL_DB_HOST"),
            port=getenv("MYSQL_DB_PORT"),
            db=getenv("MYSQL_DB_NAME")
        )
        if setup_database(engine):
            logger.info("Banco de dados configurado com sucesso!")
            complete_task = True
        else:
            logger.info("Tentativa %s estabelecer conexão com o banco de dados" % tries)
            sleep(time_sleep)

    if not complete_task:
        logger.error("Não foi possivel configurar o banco de dados")
        exit(1)
    exit(0)
