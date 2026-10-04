from mysite.database.models import Group,GroupPeople,GroupMessage
from sqladmin import ModelView


class GroupAdmin(ModelView,model = Group):
    column_list = [Group.group_name]



class GroupPeopleAdmin(ModelView,model = GroupPeople):
    column_list = [GroupPeople.group_id]



class GroupMessageAdmin(ModelView,model = GroupMessage):
    column_list = [GroupMessage.group_id,GroupMessage.message]