from django.urls import path

from . import views

"""
TODO [задачки]
Прочитай про то какие должны быть url'ы в REST API и сделай по красоте)
https://habr.com/ru/articles/351890/
https://tproger.ru/translations/luchshie-praktiki-razrabotki-rest-api-20-sovetov
И сам еще поищи что-нибудь
"""
urlpatterns = [
    path("lib/<int:library_id>", views.library_api, name="library"),
    path("book/<str:book_name>", views.book_api, name="book"),  # TODO [замечание] Лучше все таки сделать здесь id, а не название

]
