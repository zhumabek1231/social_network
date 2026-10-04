import uvicorn
from fastapi import FastAPI
from mysite.api import stories, stories_like, stories_comment,predict

stories_app = FastAPI(title="Stories API")

stories_app.include_router(stories.router)
stories_app.include_router(stories_like.router)
stories_app.include_router(stories_comment.router)
stories_app.include_router(predict.cifar_router)


if __name__ == '__main__':
    uvicorn.run(stories_app, host = '127.0.0.1',port = 8003)

