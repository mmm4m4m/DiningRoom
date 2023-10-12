from fastapi import FastAPI

from users.routers import router as user_router

app = FastAPI(title='Dining room')

app.include_router(router=user_router)
