from typing import Optional

import pytest 
from fastapi.testclient import TestClient

from src.main import app
from src.users.utils import get_hashed_password
from src.database.db import DBManager, get_db_manager, create_database, drop_database
from tests.config import TEST_DATABASE_DIR


@pytest.fixture(scope='session', autouse=True)
def db_setup():
    create_database(TEST_DATABASE_DIR)

    def override_get_db_manager():
        db_manager = DBManager()
        db_manager.connect(TEST_DATABASE_DIR)
        return db_manager
    
    app.dependency_overrides[get_db_manager] = override_get_db_manager
    yield 
    drop_database(TEST_DATABASE_DIR)


@pytest.fixture
def db_manager() -> DBManager:
    db_manager_ = DBManager()
    db_manager_.connect(TEST_DATABASE_DIR)
    yield db_manager_
    db_manager_.rollback()
    db_manager_.close()


@pytest.fixture 
def client():
    return TestClient(app)


@pytest.fixture
def user(db_manager) -> dict:
    hashed_password = get_hashed_password('12345678')
    params = (hashed_password, )
    db_manager.execute('INSERT INTO users(email, hashed_password) '
                       'VALUES("test@test.com", ?) ', 
                       params=params)
    test_user = db_manager.execute('SELECT * FROM users WHERE email="test@test.com"')
    return {'id': test_user[0], 'email': test_user[1], 'hashed_password': test_user[2]}


@pytest.fixture 
def product(db_manager) -> dict:
    db_manager.execute('INSERT INTO products(id, name) '
                       'VALUES(100, "Apple") ')
    test_product = db_manager.execute('SELECT * FROM products WHERE id=100')
    return {'id': test_product[0], 'name': test_product[1]}
