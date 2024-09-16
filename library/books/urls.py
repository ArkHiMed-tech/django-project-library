from django.urls import path

from . import views

"""
TODO [задачки]
все url'ы должны заканчиваться /, зафикси
"""
urlpatterns = [
    path("libraries/<int:id>", views.LibraryView.as_view(), name="library"),
    path("libraries/books/<int:id>", views.LibraryBooks.as_view(), name="library_book_list"), # todo: не очень хороший url, перечитай методичку)
    path("libraries/", views.LibraryList.as_view(), name="libraries_list"),
    path("books/<int:id>", views.BookView.as_view(), name="book"),
    path("books/", views.BookList.as_view(), name="books_list"),

]
