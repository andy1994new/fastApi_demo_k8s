from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# this is only for local test
# SQLALCHEMY_DATABASE_URL = "postgresql://andyg:@localhost:5432/postgres"

# this is for the dock compose test
SQLALCHEMY_DATABASE_URL = "postgres://user:password@db:5432/postgres"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

User_Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = User_Session()
    try:
        yield db
    finally:
        db.close()
