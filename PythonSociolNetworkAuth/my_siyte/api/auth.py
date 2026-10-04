from fastapi import APIRouter, HTTPException, Depends,status
from my_siyte.database.db import SessionLocal
from my_siyte.database.model import UserProfile,RefreshToken
from my_siyte.database.shema import UserProfileInputShem , UserProfileOutShema ,UserLoginSchema,CurrentUserSchema
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi. security import OAuth2PasswordBearer
from my_siyte.conf import  (SECRET_KEY,ALGORITHM,ACCESS_TOKEN_LIFETIME,REFRESH_TOkEN_LIFETIME)
from datetime import timedelta,datetime
from jose import jwt, JWTError
from typing import Optional
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oath2_schema = OAuth2PasswordBearer (tokenUrl="/auth/login")

auth_router = APIRouter (prefix='/auth', tags=['Auth'])
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db. close()

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)
async def get_current_user(token: str = Depends(oath2_schema),db:Session = Depends(get_db),):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        subject = payload.get("sub")
        if subject is None:
            raise credentials_exception

        user_id =int(subject)

    except (JWTError,TypeError,ValueError):
        raise credentials_exception
    user_db = (
        db.query(UserProfile)
        .filter(UserProfile.id == user_id)
        .first()
    )
    if not user_db:
        raise credentials_exception
    return user_db
def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password (plain_password, hashed_password):
     return pwd_context.verify(plain_password, hashed_password)

def create_access_token (data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data. copy()
    expires = datetime.utcnow()  + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_LIFETIME))
    to_encode.update({"exp": expires})
    return jwt. encode (to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict):
    return create_access_token (data, expires_delta=timedelta(days=REFRESH_TOkEN_LIFETIME))



@auth_router.post( '/register/', response_model=dict)
async def register(user: UserProfileInputShem , db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.username==user.username).first()
    email_db = db.query(UserProfile).filter(UserProfile.email==user.email).first()
    if user_db or email_db:
            raise HTTPException(detail='Mындай username жe почта бap экен',status_code=400)
    hash_password = get_password_hash(user.password)
    user_data=UserProfile(
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        email=user.email,
        phone_number=user.phone_number,
        password=hash_password,
        age=user.age,

    )
    db.add(user_data)
    db.commit()
    db.refresh(user_data)
    return {'message': 'Сиз регистрация болдунуз'}

#
# @auth_router.post( '/login/', response_model=dict)
# async def login (user: UserLoginSchema , db: Session = Depends (get_db)):
#     user_db = db. query (UserProfile). filter (UserProfile. username==user. username).first ()
#     if not user_db or not verify_password (user.password, user_db.password):
#         raise HTTPException(detail='Сиз жазган маалымат туура эмес',status_code=401)
#
#     access_token = create_access_token ({'sub': user_db.username})
#     refresh_token = create_refresh_token({'sub': user_db.username})
#
#     token_db = RefreshToken(user_id=user_db.id, token=refresh_token)
#     db.add(token_db)
#     db.commit()
#
#     return {'access_token': access_token,'refresh_token':refresh_token,'token_type':'Bearer'}



@auth_router.post('/logout')
async def logout (refresh_token: str, db: Session = Depends (get_db)):
    stored_token = db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()

    if not stored_token:
        raise HTTPException(status_code=401, detail="Маалымат туура эмес")
    db. delete (stored_token)
    db. commit ()
    return {"message": "Bbunu"}

def get_token_data (user: UserProfile):
      return {'sub': str (user.id), 'username': user.username, 'is_official': user.is_official}

@auth_router.post ('/login/', response_model=dict)
async def login (user: UserLoginSchema, db: Session = Depends(get_db)):
       user_db = (db.query (UserProfile).filter (UserProfile.username == user.username).first())
       if not user_db or not verify_password (user. password, user_db. password):
            raise HTTPException (detail='Сиз жазган маалымат туура эмес',status_code=401)
       token_data = get_token_data(user_db)

       access_token = create_access_token (token_data)
       refresh_token = create_refresh_token(token_data)
       token_db= RefreshToken(user_id=user_db.id, token=refresh_token)
       db. add (token_db)
       db. commit()
       return {'access_token': access_token, 'refresh_token': refresh_token, 'token_type': 'Bearer'}

#
# @auth_router.post('/refresh')
# async def refresh(refresh_token: str, db: Session = Depends (get_db)) :
#     stored_token = db.query (RefreshToken). filter (RefreshToken. token == refresh_token). first()
#     if not stored_token:
#         raise HTTPException (status_code=401, detail="Maaлымат тyypa эмec")
#
#     access_token = create_access_token({"sub": stored_token.id})
#     return {"access_token": access_token, "token_type": "bearer"}


@auth_router.get ('/verify/', response_model=CurrentUserSchema)
async def verify_access_token (current_user: UserProfile = Depends(get_current_user)):
     return current_user