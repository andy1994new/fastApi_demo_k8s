# database.py
"""
This module contains the database configuration and session management for the application.
It defines the connection to the PostgreSQL database -
and provides a sessionmaker for interacting with the database.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL is the connection string for the PostgreSQL database.
# For local testing:
# SQLALCHEMY_DATABASE_URL = "postgresql://andyg:@localhost:5432/postgres"
# For the Docker Compose setup:
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@db:5432/app_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

Product_Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Dependency function to get a database session.

    This function can be used as a dependency in FastAPI routes to provide a
    database session for each request. It ensures that the session is closed
    after the request is processed.

    Returns:
        Session: A SQLAlchemy session object.
    """
    db = Product_Session()
    try:
        yield db
    finally:
        db.close()
