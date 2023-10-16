from src.products.resolvers import get

def test_get_product(db_manager, client):
    db_manager.execute('INSERT INTO products VALUES(50, "Avocado")')
    db_manager.commit()
    response = client.get('/products/50')
    assert response.status_code == 200, 'Ошибка запроса'
    product = response.json()['data']
    assert product['id'] == 50, 'Получен неверный продукт'


def test_update_product(db_manager, client):
    db_manager.execute('INSERT INTO products VALUES(40, "Coconut")')
    db_manager.commit()
    response = client.put('/products/40', json={'name': 'Tomato'})
    assert response.status_code == 200, 'Ошибка запроса'
    assert response.json()['detail'] == 'Продукт обновлен'
