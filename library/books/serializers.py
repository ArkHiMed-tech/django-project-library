from rest_framework import serializers
from .models import Library, Book


class LibrarySerialiser(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = ['id', 'address']


class BookSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['name', 'author', 'creation_date', 'library', 'file']


class DummyDetailSerializer(serializers.Serializer):
    status = serializers.IntegerField()


class DummyDetailAndStatusSerializer(serializers.Serializer):
    status = serializers.IntegerField()
    details = serializers.CharField()