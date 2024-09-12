from django.shortcuts import render
from django.http import JsonResponse
from django.forms.models import model_to_dict
from .models import Library, Book

# Create your views here.
def library_api(request, library_id):
    """
    TODO [задачки]
    1) Сделать с помощью view из drf
    2) Сделать все CRUD методы
    3) Сделать метод для просмотра списка
    4) Сделать метод для просмотра всех книг в этой библиотеке
    """
    try:
        return JsonResponse(model_to_dict(Library.objects.get(id=library_id)))
    except Library.DoesNotExist:
        return JsonResponse('Lib not found', safe=False)
    
def book_api(request, book_name):
    """
    TODO [задачки]
    1) Сделать с помощью view из drf
    2) Сделать все CRUD методы
    3) Сделать метод для просмотра списка
    4) Сделать фильтры (чтобы можно было фильтровать по полям)
    """
    try:
        return JsonResponse(model_to_dict(Book.objects.get(name=book_name)))
    except Book.DoesNotExist:
        return JsonResponse('Book not found', safe=False)

