#!coding:utf8
from django.urls import path
from .views import RobotInboundView


urlpatterns = [
    path("<uuid>/inbound", RobotInboundView.as_view())
]