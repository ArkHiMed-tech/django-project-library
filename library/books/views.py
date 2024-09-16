from django.shortcuts import render
from django.http import JsonResponse
from django.forms.models import model_to_dict

from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import status

from .models import Library, Book
from .serializers import LibrarySerialiser, BookSerialiser

"""
TODO[правки]:
Везде добавь поле id для библиотеки
"""
class LibraryList(APIView):
    def get(self, request, format=None):
        snippets = Library.objects.all()
        serializer = LibrarySerialiser(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        print(request.data)
        serializer = LibrarySerialiser(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LibraryView(APIView):
    def get_object(self, id):
        # todo [замечание]: это странный способ, но в целом рабочий, лучше перенести это в какой-нибудь LibraryMixin, погугли что такое Mixin в джанго
        try:
            return Library.objects.get(id=id)
        except Library.DoesNotExist:
            raise Http404
        
    def get(self, request, id):
        lib = self.get_object(id)
        serialiser = LibrarySerialiser(lib)
        return Response(serialiser.data)
    
    def put(self, request, id):
        lib = self.get_object(id)
        serializer = LibrarySerialiser(lib, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        lib = self.get_object(id)
        lib.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LibraryBooks(APIView):
    def get(self, request, id):
        books = []
        for i in BookSerialiser(Book.objects.all(), many=True).data:  # todo: почитай доку django orm, это плохой способ, а еще сериалайзер тут кривоватый)
            if i['library'] == id:
                books.append(i)
        return Response(books)  # todo: сериалайзер лучше здесь


class BookList(APIView):
    def get(self, request, format=None):
        if len(request.GET) >= 0:
            books = Book.objects.filter(**request.GET.dict())
            serializer = BookSerialiser(books, many=True)
        else:
            books = Book.objects.all()
            serializer = BookSerialiser(books, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = BookSerialiser(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookView(APIView):
    def get_object(self, id):
        try:
            return Book.objects.get(id=id)
        except Book.DoesNotExist:
            raise Http404
        
    def get(self, request, id):
        book = self.get_object(id)
        serialiser = BookSerialiser(book)
        return Response(serialiser.data)
    
    def put(self, request, id):
        book = self.get_object(id)
        serializer = BookSerialiser(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        book = self.get_object(id)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



def library_api(request, library_id):
    """
    TODO [правки]
    А зачем тебе эта функция? Если не используешь - убери
    """
    try:
        return JsonResponse(model_to_dict(Library.objects.get(id=library_id)))
    except Library.DoesNotExist:
        return JsonResponse('Lib not found', safe=False)
    
def book_api(request, book_id):
    """
    TODO [правки]
    А зачем тебе эта функция? Если не используешь - убери
    """
    try:
        return JsonResponse(model_to_dict(Book.objects.get(id=book_id)))
    except Book.DoesNotExist:
        return JsonResponse('Book not found', safe=False)

