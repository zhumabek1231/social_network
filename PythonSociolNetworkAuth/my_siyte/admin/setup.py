from .view import UserProfileAdmin
from fastapi import FastAPI
from sqladmin import Admin
from my_siyte.database.db import engine


def setup_admin(auth_app: FastAPI):
    admin = Admin(auth_app,engine)
    admin.add_view(UserProfileAdmin)