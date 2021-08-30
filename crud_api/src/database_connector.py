import logging
import sqlalchemy
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.engine import Engine
from os import getenv, environ

if not getenv('CONTEXT', 'LOCAL') == 'CONTAINER':
    environ["MYSQL_DB_USER"] = 'root'
    environ["MYSQL_DB_PASSWORD"] = 'encn9dgo'
    environ["MYSQL_DB_HOST"] = 'localhost'
    environ["MYSQL_DB_PORT"] = '8083'
    environ["MYSQL_DB_NAME"] = 'ibge'


class MysqlHook:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._connection = None
        self.is_connected = False
        self.user = getenv("MYSQL_DB_USER")
        self.password = getenv("MYSQL_DB_PASSWORD")
        self.host = getenv("MYSQL_DB_HOST")
        self.port = getenv("MYSQL_DB_PORT")
        self.db = getenv("MYSQL_DB_NAME")
        self.db_engine = None
        self.db_session = None

    def get_database_engine(self) -> Engine:
        connection_str = 'mysql+pymysql://'
        connection_str += f'{self.user}:{self.password}@{self.host}:{self.port}/{self.db}'
        try:
            self.db_engine = sqlalchemy.create_engine(connection_str,
                                                      pool_size=1,
                                                      echo=False,
                                                      connect_args={
                                                          'connect_timeout': 30
                                                      },
                                                      execution_options={
                                                          "isolation_level": "AUTOCOMMIT"
                                                      }
                                                      )

            return self.db_engine
        except OperationalError as error:
            self.logger.error("Não foi possivel criar engine de conexão com o banco de dados. Detalhes:")
            self.logger.error(error)
            raise error

    def create_session(self) -> Session:
        if self.db_engine:
            self.db_session = sessionmaker(self.db_engine)()
            return self.db_session
        else:
            self.db_session = sessionmaker(self.get_database_engine)()
            return self.db_session

    def __del__(self):
        if self.db_session:
            if self.db_session.is_active:
                self.db_session.commit()
                self.db_session.close()