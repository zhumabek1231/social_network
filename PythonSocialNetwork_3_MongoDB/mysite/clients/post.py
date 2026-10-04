import httpx
from fastapi import HTTPException
from mysite.conf import settings


async def get_object (url: str):
    try:
        async with httpx.AsyncClient(timeout=5) as client:
             response = await client.get(url)
    except httpx.RequestError:
        raise HTTPException (status_code=500, detail='Post Service недоступен')

    if response.status_code == 404:
        raise HTTPException(status_code=404, detail='страница не найдена')


    if response.status_code != 200:
        raise HTTPException(status_code=500, detail='ошибка в service 2')


    try:
        return response.json()
    except ValueError:
        raise HTTPException(status_code=500, detail='Неправильные данные')

async def get_post(post_id: int):
     url = f'{settings.post_service_url}/post/{post_id}/'
     return await get_object(url=url)

