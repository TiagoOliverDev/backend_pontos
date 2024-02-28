import psycopg2
import os
import logging

class Db:
    def __init__(self):
        self.db_config = {
            "dbname": os.environ.get('DB_DATABASE'),
            "user": os.environ.get('DB_USER'),
            "password": os.environ.get('DB_PASSWORD'),
            "port": os.environ.get('DB_PORT'),
            "host": os.environ.get('DB_HOST')
        }

    def connect(self, process: str):
        try:
            connection = psycopg2.connect(**self.db_config)
            logging.info(f"Conexão com o banco de dados estabelecida com sucesso. Processo: {process}")
            return connection
        except psycopg2.Error as e:
            logging.error(f"Erro ao conectar com o banco de dados: {e}")
            return None

    def disconnect(self, conn):
        try:
            if conn:
                conn.close()
                logging.info("Banco de dados desconectado com sucesso!")
            else:
                logging.warning("Não recebemos uma conexão válida para desconectar")
        except psycopg2.Error as e:
            logging.error(f"Erro ao desconectar do banco de dados: {e}")
