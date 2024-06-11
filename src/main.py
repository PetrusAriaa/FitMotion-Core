from fastapi import FastAPI

from .routes import classifier_router, friends_router, user_router, auth_router

app = FastAPI()

@app.get('/health', tags=['Healthcheck'])
def ping():
    return {"message": "pong"}

app.include_router(prefix='/api/v1/predict', router=classifier_router)
app.include_router(prefix='/api/v1/friends', router=friends_router)
app.include_router(prefix='/api/v1/users', router=user_router)
app.include_router(prefix='/auth', router=auth_router)