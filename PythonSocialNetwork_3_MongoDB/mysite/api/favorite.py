from fastapi import APIRouter,Depends,HTTPException
from mysite.database.mongodb import get_favorite_collection,get_favorite_item_collection
from mysite.shemas.favorite import FavoriteCreate,FavoriteItemCreate,FavoriteItemResponse,FavoriteResponse
from mysite.database.mapper import favorite_document_to_response,favorite_item_document_to_response
from mysite.api.dependencies import get_current_user
from typing import Annotated,List
from datetime import date,datetime,time,timezone
from mysite.clients.post import get_post
import asyncio
from fastapi import APIRouter, Depends, status

network_router = APIRouter(prefix='/favorite',tags=['Favorite'])





@network_router.get('/', response_model=List[FavoriteResponse])
async def get_favorites(current_user: Annotated[dict, Depends(get_current_user)]):
    collection = get_favorite_collection()


    cursor = collection.find({'user_id': current_user['id']}).sort('created_at', -1)


    favorites = [favorite_document_to_response(doc) async for doc in cursor]
    return favorites


@network_router.post('/', response_model=FavoriteResponse, status_code=status.HTTP_201_CREATED)
async def favorite_create(
        favorite: FavoriteCreate,
        current_user: Annotated[dict, Depends(get_current_user)]
):
    collection = get_favorite_collection()


    favorite_dict = {
        "user_id": current_user["id"],
        "name": favorite.name,
        "created_at": datetime.now(timezone.utc)
    }


    result = await collection.insert_one(favorite_dict)
    favorite_dict["_id"] = result.inserted_id

    return favorite_document_to_response(favorite_dict)




@network_router.post("/items", response_model=FavoriteItemResponse, status_code=status.HTTP_201_CREATED)
async def add_favorite_item(item: FavoriteItemCreate,current_user: Annotated[dict, Depends(get_current_user)]):

    collection = get_favorite_item_collection()

    item_document = {
        "favorite_id": item.favorite_id,
        "content_id": item.content_id,
        "status": item.status.value,
        "created_at": datetime.now(timezone.utc)
    }

    result = await collection.insert_one(item_document)
    item_document["_id"] = result.inserted_id

    return favorite_item_document_to_response(item_document)


@network_router.get("/items/{favorite_id}", response_model=List[FavoriteItemResponse])
async def get_favorite_items(favorite_id: str,current_user: Annotated[dict, Depends(get_current_user)]):

    collection = get_favorite_item_collection()
    cursor = collection.find({"favorite_id": favorite_id}).sort("created_at", -1)

    return [favorite_item_document_to_response(doc) async for doc in cursor]













