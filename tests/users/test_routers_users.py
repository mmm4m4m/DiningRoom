from src.users.resolvers import create
from src.users.models import UserInput, UserCreate


def test_create(client):
    user_in = {'email': 'new_user@example.com', 'password': '12345678'}
    response = client.post('/register', json=user_in)
    assert response.status_code == 200, 'Ошибка запроса'
    created_user = response.json()['data']
    assert created_user['email'] == 'new_user@example.com', 'Пользователь был создан с неверными данными'


def test_login(db_manager, client):
    user_in = UserInput(email='testuser@example.com', password='12345678')
    create(db_manager=db_manager, user_in=user_in)
    db_manager.commit()
    response = client.post('/login', json={'email': user_in.email, 'password': '12345678'})
    assert response.status_code == 200, 'Ошибка запроса'
    user = response.json()['data']
    assert user['email'] == 'testuser@example.com', 'Получен неверный пользователь'


def delete_user(db_manager, client):
    user_in = UserCreate(email='testuser1@example.com', password='12345678')
    create(db_manager=db_manager, user_in=user_in)
    db_manager.commit()
    response = client.delete(f'/{user_in.email}')
    assert response.status_code == 200, 'Ошибка запроса'
    assert response.json()['detail'] == 'Пользователь удален', 'Пользователь не был удален'
    