from django.urls import path

from . import views

urlpatterns = [
    path("libraries/<int:id>/", views.LibraryView.as_view(), name="library"),
    path("libraries/<int:id>/books/", views.LibraryBooks.as_view(), name="library_book_list"),
    path("libraries/", views.LibraryList.as_view(), name="libraries_list"),
    path("books/<int:id>/", views.BookView.as_view(), name="book"),
    path("books/", views.BookList.as_view(), name="books_list"),

]
