import os
import jaydebeapi
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class DenodoIntegration:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.connect()

    def connect(self):
        try:
            denodo_host = os.getenv("DENODO_HOST")
            denodo_port = os.getenv("DENODO_PORT")
            denodo_database = os.getenv("DENODO_DATABASE")
            denodo_username = os.getenv("DENODO_USERNAME")
            denodo_password = os.getenv("DENODO_PASSWORD")
            denodo_jdbc_driver = os.getenv("DENODO_JDBC_DRIVER")

            url = f"jdbc:denodo://{denodo_host}:{denodo_port}/{denodo_database}"
            self.connection = jaydebeapi.connect(
                "com.denodo.vdp.jdbc.Driver",
                url,
                [denodo_username, denodo_password],
                denodo_jdbc_driver
            )
            self.cursor = self.connection.cursor()
            logger.info("Connected to Denodo successfully")
        except Exception as e:
            logger.error(f"Failed to connect to Denodo: {str(e)}")
            raise

    def execute_query(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            result = self.cursor.fetchall()
            return result
        except Exception as e:
            logger.error(f"Failed to execute query: {str(e)}")
            raise

    def close(self):
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
            logger.info("Closed Denodo connection")
        except Exception as e:
            logger.error(f"Failed to close Denodo connection: {str(e)}")
            raise
