from django.urls import path


from . import views


urlpatterns = [
    path("app/<int:app_id>/message/verify", views.MessageReceiveView.as_view())
]
