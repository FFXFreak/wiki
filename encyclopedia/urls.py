from django.urls import path

from . import views
app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:req_entry>", views.entry, name="entry"),
    path("search", views.search, name="search"),
    path("new_page", views.newPage, name="newPage"),
    path("edit_page/<str:req_entry>", views.editPage, name="editPage"),
    path("random", views.randomPage, name="random")
]
