from my_siyte.database.model import UserProfile
from sqladmin import ModelView


class UserProfileAdmin(ModelView,model = UserProfile):
    column_list = [UserProfile.first_name,UserProfile.last_name]