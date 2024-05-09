# Third Party
from django.urls import path

# Local Folder
from . import views

app_name = "user"
urlpatterns = [
    path("", views.UserView.as_view(), name="add_user"),
    path("<uuid:pk>", views.UserView.as_view(), name="user"),
]
