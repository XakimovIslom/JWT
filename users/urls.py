from django.urls import path

from users.api.views import UserRegisterView, LoginView
from users.views import user_detail_view, user_redirect_view, user_update_view

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),

    path('register/', UserRegisterView.as_view()),
    path('login/', LoginView.as_view()),
]
