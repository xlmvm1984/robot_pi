from django.contrib import admin
from .models import User


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'user_type', 'gender_name', "enterprise_wechat_user"]

    def gender_name(self, item):
        names = {0: "unknown", 1: "male", 2: "female"}
        return names.get(item.gender)
