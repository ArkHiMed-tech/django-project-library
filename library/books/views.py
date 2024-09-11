from django.shortcuts import render
from django.http import JsonResponse
from django.forms.models import model_to_dict
from .models import Library, Book

# Create your views here.
def library_api(request, library_id):
    try:
        return JsonResponse(model_to_dict(Library.objects.get(id=library_id)))
    except Library.DoesNotExist:
        return JsonResponse('Lib not found', safe=False)
    
def book_api(request, book_name):
    try:
        return JsonResponse(model_to_dict(Book.objects.get(name=book_name)))
    except Book.DoesNotExist:
        return JsonResponse('Book not found', safe=False)