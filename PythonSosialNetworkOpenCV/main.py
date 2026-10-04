from fastapi import FastAPI
import uvicorn
from opencv import network_app


check_image_app = FastAPI()
check_image_app.include_router(network_app.router)
if __name__ == '__main__':
     uvicorn.run(check_image_app,host='127.0.0.1',port=8000)
