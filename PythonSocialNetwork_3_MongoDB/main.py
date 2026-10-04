from fastapi import FastAPI,HTTPException
import uvicorn
from pymongo.errors import PyMongoError
from mysite.api import favorite
from mysite.database.mongodb import close_mongodb,connect_mongodb,get_database
from contextlib import asynccontextmanager




@asynccontextmanager
async def lifespan (app: FastAPI):
    try:
         await connect_mongodb()
         print ('Mongodb: подключено усспешно')
         yield
    finally:
         await close_mongodb()
         print ('Mongodb: соединение закрыто ' )


favorite_app = FastAPI(title='Favorite Service',lifespan=lifespan)
favorite_app.include_router(favorite.network_router)

# @booking_app.get('/')
# async def test_info():
#     return {'message':'Все работает'}
@favorite_app.get('/check/database/')
async def check_database():
    try:
        database = get_database()
        await database.command('ping')

        return {'status': 'ok', 'database': database.name, 'connection': 'active'}

    except PyMongoError:
         raise HTTPException(status_code=500, detail='Mongodb Недоступен')






if __name__=='__main__':
    uvicorn.run(favorite_app,host='127.0.0.1',port=8002)