
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database URL format for MySQL
# Format: "mysql+pymysql://<username>:<password>@<host>/<database_name>"
DATABASE_URL = "mysql+pymysql://root@localhost/test"

# Create an engine
engine = create_engine(DATABASE_URL)

# Create a session local class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models
Base = declarative_base()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# sqlite connection
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

# # Database URL
# DATABASE_URL = "sqlite:///./test.db"  # Change this to your desired database file

# # Create an engine
# engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# # Create a session local class
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # Base class for declarative models
# Base = declarative_base()

# # Dependency to get the database session
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
