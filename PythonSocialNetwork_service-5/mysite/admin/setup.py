from .views import GroupAdmin,GroupPeopleAdmin,GroupMessageAdmin
from fastapi import FastAPI
from sqladmin import Admin
from mysite.database.db import engine


def setup_admin(auth_app: FastAPI):
    admin = Admin(auth_app,engine)
    admin.add_view(GroupAdmin)
    admin.add_view(GroupPeopleAdmin)
    admin.add_view(GroupMessageAdmin)