from fastapi import FastAPI

from src.users.routers import router as users_router
from src.products.routers import router as products_router
from src.dishes.routers import router as dishes_router


app = FastAPI(title='Dining room')

app.include_router(router=users_router)
app.include_router(router=products_router)
app.include_router(router=dishes_router)
