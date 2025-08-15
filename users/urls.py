from django.urls import path

from users.views import UserListView, UserRegistrationView

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="user-registration"),
    path("", UserListView.as_view(), name="user-list"),
]
