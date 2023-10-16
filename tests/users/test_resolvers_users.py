from src.users.resolvers import get, get_user_by_email, create, delete
from src.users.models import UserInput


def test_get(user, db_manager):
    user_id = user['id']
    test_user = get(db_manager=db_manager, user_id=user_id)
    assert test_user is not None, 'Функция не возвратила пользователя'
    assert test_user.id == user_id, 'Функция возвратила не того пользователя'


def test_get_user_by_email(user, db_manager):
    user_email = user['email']
    test_user = get_user_by_email(db_manager=db_manager, email=user_email)
    assert test_user is not None, 'Функция не возвратила пользователя'
    assert test_user.email == user_email, 'Функция возвратила не того пользователя'


def test_create(db_manager):
    user_in = UserInput(email='new_user@test.com', password='12345678')
    create(db_manager=db_manager, user_in=user_in)
    created_user = get_user_by_email(db_manager=db_manager, email='new_user@test.com')
    assert created_user is not None, 'Пользователь не был создан'
    assert created_user.email == user_in.email, 'Пользователь был создан с неверными данными'


def test_delete(user, db_manager):
    user_email = user['email']
    delete(db_manager=db_manager, user_email=user_email)
    deleted_user = get_user_by_email(db_manager=db_manager, email=user_email)
    assert deleted_user is None, 'Пользователь не был удален'
