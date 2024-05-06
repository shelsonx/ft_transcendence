# Third Party
from django.urls import path

# Local Folder
from . import views

app_name = "user"
urlpatterns = [
    path("add", views.UserView.as_view(), name="add_user"),
    path("edit/<uuid:pk>", views.UserView.as_view(), name="edit_user"),
    path("delete/<uuid:pk>", views.UserView.as_view(), name="delete_user"),
]
