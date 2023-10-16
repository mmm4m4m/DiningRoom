from src.database.db import get_db_manager 

db_manager =get_db_manager()

res = db_manager.execute('SELECT * FROM product_dish', many=True)
print(res)