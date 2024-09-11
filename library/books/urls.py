from django.urls import path

from . import views

urlpatterns = [
    path("lib/<int:library_id>", views.library_api, name="library"),
    path("book/<str:book_name>", views.book_api, name="book"),
]
