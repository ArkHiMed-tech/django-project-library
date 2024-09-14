from django.urls import path

from . import views

"""
TODO [задачки]
Прочитай про то какие должны быть url'ы в REST API и сделай по красоте) --OK
https://habr.com/ru/articles/351890/
https://tproger.ru/translations/luchshie-praktiki-razrabotki-rest-api-20-sovetov
И сам еще поищи что-нибудь
"""
urlpatterns = [
    path("libraries/<int:id>", views.LibraryView.as_view(), name="library"),
    path("libraries/books/<int:id>", views.LibraryBooks.as_view(), name="library_book_list"),
    path("libraries/", views.LibraryList.as_view(), name="libraries_list"),
    path("books/<int:id>", views.BookView.as_view(), name="book"),
    path("books/", views.BookList.as_view(), name="books_list"),

]
