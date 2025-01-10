from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# this is only for local test
# SQLALCHEMY_DATABASE_URL = "postgresql://andyg:@localhost:5432/postgres"

# this is for the dock compose test
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@db:5432/app_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

User_Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = User_Session()
    try:
        yield db
    finally:
        db.close()
