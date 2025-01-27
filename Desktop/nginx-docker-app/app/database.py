import mysql.connector
from config import Config
from contextlib import contextmanager
from typing import List, Dict, Any, Optional
import logging

class Database:
    @contextmanager
    def connection(self):
        """Creates and manages database connection"""
        logging.debug(f"Attempting to connect to MySQL at {Config.DB_HOST}") 
        conn = mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )
        logging.debug("Connected to MySQL successfully!")
        try:
            yield conn
        finally:
            conn.close()
            logging.debug("Connection closed")

    def execute_query(self, query: str, params: Optional[tuple] = None) -> None:
        """Executes a database query with optional parameters"""
        with self.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                conn.commit()
                logging.debug("Query executed successfully")
                logging.debug(f"Query: {query}")
                logging.debug(f"Params: {params}")

    def fetch_query(self, query: str) -> List[Dict[str, Any]]:
        """Executes SELECT query and returns list of dictionaries with results"""
        with self.connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                logging.debug("Fetch query successful")
                logging.debug(f"Query: {query}")
                logging.debug(f"Result: {result}")
                return result