from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("register/", views.register_view),
    path("login/", TokenObtainPairView.as_view()),   
    path("refresh/", TokenRefreshView.as_view()),
    path("send-message/", views.send_message_view),
    path("get-messages/", views.get_all_messages)
]