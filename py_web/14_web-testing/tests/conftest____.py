# import pytest
# from unittest.mock import patch
#
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
#
# from src.entity.models import Base
# from src.schemas.user import User
#
# TEST_DATABASE_URL = "sqlite:///./test.db "
#
# @pytest.fixture
# def test_db():
#     engine = create_engine(TEST_DATABASE_URL)
#
#     Base.metadata.create_all(engine)
#
#     TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#     db = TestingSessionLocal()
#
#     yield db
#
#     Base.metadata.drop_all(bind=engine)
#     db.close()
