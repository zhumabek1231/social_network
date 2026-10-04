import uvicorn
from fastapi import FastAPI
from mysite.api import group,group_people,group_message,websocket_chat
from mysite.admin.setup import setup_admin
from fastapi.staticfiles import StaticFiles
import os




group_app = FastAPI(title='Social_Network')
group_app.include_router(group.group_router)
group_app.include_router(group_message.group_message_router)
group_app.include_router(group_people.group_people_router)
group_app.include_router(websocket_chat.websocket_router)
setup_admin(group_app)
os.makedirs("uploads", exist_ok=True)
group_app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

if __name__ == '__main__':
    uvicorn.run(group_app, host = '127.0.0.1',port = 8005)