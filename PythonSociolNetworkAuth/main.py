import uvicorn
from fastapi import FastAPI
from my_siyte.api import user,auth
from my_siyte.admin.setup import setup_admin



auth_app = FastAPI(title='Social_Network')
auth_app.include_router(user.user_router)
auth_app.include_router(auth.auth_router)
setup_admin(auth_app)

if __name__ == '__main__':
    uvicorn.run(auth_app, host = '127.0.0.1',port = 8000)