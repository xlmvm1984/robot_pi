from django.contrib import admin
from .models import RobotPi


# Register your models here.
@admin.register(RobotPi)
class RobotPiAdmin(admin.ModelAdmin):
    pass
