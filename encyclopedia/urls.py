from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("wiki/<str:title>", views.entry, name="title"),
    path("new_page", views.new_page, name="newpage"),
    path("edit_page/<str:page_title>", views.edit_page, name="editpage"),
    path("random_page", views.random_page, name="randompage")
]
