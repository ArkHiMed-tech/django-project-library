from django.shortcuts import render
from django.http import JsonResponse
from django.forms.models import model_to_dict

from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import status

from .models import Library, Book
from .serializers import LibrarySerialiser, BookSerialiser
from .utils import LibraryMixin


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


class LibraryView(LibraryMixin, APIView):        
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
        lib = Library.objects.get(id=id)
        books = Book.objects.filter(library=lib)
        return Response(BookSerialiser(books, many=True).data)


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