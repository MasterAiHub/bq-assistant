import os
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)

class DatabaseConnection:
    """Handles secure database connections"""

    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL", "sqlite:///./test.db")
        self.engine = None
        self.SessionLocal = None
        self._initialize_connection()

    def _initialize_connection(self):
        try:
            self.engine = create_engine(self.database_url)
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            logger.info(f"Database connection initialized for {self.database_url}")
        except Exception as e:
            logger.error(f"Database connection failed: {str(e)}")
            raise

    def get_db(self):
        """Dependency to get database session"""
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def execute_query(self, query: str, params: dict = None):
        """Executes a raw SQL query safely"""
        if not self.engine:
            raise ConnectionError("Database engine not initialized.")
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text(query), params)
                connection.commit()
                return result
        except Exception as e:
            logger.error(f"Error executing query: {query} - {str(e)}")
            raise

    def test_connection(self):
        """Tests the database connection"""
        try:
            with self.engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            logger.info("Database connection test successful.")
            return True
        except Exception as e:
            logger.error(f"Database connection test failed: {str(e)}")
            return False
