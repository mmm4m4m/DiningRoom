from src.products.resolvers import get, create, update, delete, get_products_by_name
from src.products.models import ProductInput, ProductUpdate


def test_get(product, db_manager):
    test_product = get(db_manager=db_manager, product_id=product['id'])
    assert test_product is not None, 'Функция не возвратила продукт'    
    assert test_product.id == product['id'], 'Функция возвратила не тот продукт'


def test_create(db_manager):
    product_in = ProductInput(name='Pineapple')
    create(db_manager=db_manager, product_in=product_in)
    created_product = get_products_by_name(db_manager=db_manager, product_name='Pineapple')
    assert created_product, 'Функция не создала новый продукт'


def test_update(product, db_manager):
    product_in = ProductUpdate(name='Orange')
    update(db_manager=db_manager, product_id=product['id'], product_in=product_in)
    updated_product = get(db_manager=db_manager, product_id=product['id'])
    assert updated_product.name == product_in.name, 'Продукт не был обновлен'


def test_delete(product, db_manager):
    delete(db_manager=db_manager, product_id=product['id'])
    deleted_product = get(db_manager=db_manager, product_id=product['id'])
    assert deleted_product is None, 'Продукт не был удален'
