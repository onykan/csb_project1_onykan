from django.urls import path
from . import views


app_name = "forum"
urlpatterns = [
    path("", views.index, name="index"),
    path("post/", views.write_post, name="compose"),
    path("post/<int:post_id>/", views.view_post, name="view"),
    path("post/<int:post_id>/edit/", views.write_post, {"edit_mode": True}, name="edit"),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout, name="logout"),
    path("search/", views.search, name="search")
]
