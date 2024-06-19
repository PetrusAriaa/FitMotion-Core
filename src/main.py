from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import classifier_router, friends_router, user_router, auth_router, static_data_router, storage_router, screening_router, activity_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
    allow_credentials=True
    )

@app.get('/health', tags=['Healthcheck'])
def ping():
    return {"message": "hello"}

app.include_router(prefix='/api/v1/predict', router=classifier_router)
app.include_router(prefix='/api/v1/friends', router=friends_router)
app.include_router(prefix='/api/v1/activities', router=activity_router)
app.include_router(prefix='/api/v1/users', router=user_router)
app.include_router(prefix='/auth', router=auth_router)
app.include_router(prefix='/api/v1/static', router=static_data_router)
app.include_router(prefix='/api/v1/storage', router=storage_router)
app.include_router(prefix='/api/v1/screening', router=screening_router)