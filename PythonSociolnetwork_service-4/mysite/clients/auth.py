import httpx
from fastapi import HTTPException,status
from mysite.conv import settings


async def verify_access_token(token:str):
    try:
        async with httpx.AsyncClient(timeout=5) as client:
             response = await client.get(f'{settings.auth_service_url}/auth/verify/',
                                    headers={'Authorization': f'Bearer {token}'})
    except httpx.RequestError:
        raise HTTPException(status_code=500, detail='Auth service не доступно')

    if response.status_code == 401:
        raise HTTPException(status_code=401,detail='Access token неправильный или просрочен')

    if response.status_code != 200:
        raise HTTPException(status_code=503,detail='ошибка')

    user_data = response.json()

    return {
        'id':int(user_data['id']),
        'username':user_data['username'],
    }