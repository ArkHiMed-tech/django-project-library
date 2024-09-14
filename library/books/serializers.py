from rest_framework import serializers
from .models import Library, Book


class LibrarySerialiser(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = ['address']


class BookSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['name', 'author', 'creation_date', 'library', 'file']