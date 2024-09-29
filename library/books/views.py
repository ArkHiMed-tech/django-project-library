from django.shortcuts import render
from django.http import JsonResponse
from django.forms.models import model_to_dict

from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import status
from drf_spectacular.utils import extend_schema, extend_schema_view
from drf_spectacular.utils import OpenApiExample, OpenApiResponse, OpenApiParameter

from .models import Library, Book
from .serializers import LibrarySerialiser, BookSerialiser
from .serializers import DummyDetailSerializer, DummyDetailAndStatusSerializer
from .utils import LibraryMixin


@extend_schema(tags=['Library'])
@extend_schema_view()
class LibraryList(APIView):
    @extend_schema(
            summary='Get list of all libraries', 
            responses={
                status.HTTP_200_OK: LibrarySerialiser,
                status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                    response=None,
                    description='Описание 500 ответа'
                    )
            },
            examples=[
                OpenApiExample(
                    'Get example',
                    description='Test view of all libraries',
                    value=[
                        {
                            'id': 1,
                            'address': 'Some address',
                        },
                        {
                            'id': 2,
                            'address': 'Another address',
                        }
                    ],
                    status_codes=[str(status.HTTP_200_OK)],
                    response_only=True
                )
            ]
        )
    def get(self, request, format=None):
        snippets = Library.objects.all()
        serializer = LibrarySerialiser(snippets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
            summary='Add a new library',
            responses={
                status.HTTP_201_CREATED: LibrarySerialiser,
                status.HTTP_400_BAD_REQUEST: DummyDetailAndStatusSerializer,
                status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                    response=None,
                    description='Описание 500 ответа'
                    )
            },
            examples=[
                OpenApiExample(
                    'Post example',
                    description='Both post and response example',
                    value={
                        'id': 3,
                        'address': 'Absolutely new address'
                    },
                    status_codes=[str(status.HTTP_201_CREATED)]
                )
            ]
        )
    def post(self, request, format=None):
        serializer = LibrarySerialiser(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Library'])
@extend_schema_view()
class LibraryView(LibraryMixin, APIView):
    @extend_schema(
            summary='Get information about a library',
            responses={
                status.HTTP_200_OK: LibrarySerialiser,
                status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                    response=None,
                    description='Описание 500 ответа'
                    )
            },
            examples=[
                OpenApiExample(
                    'Get example',
                    description='Test view of a library',
                    value={
                            'id': 2,
                            'address': 'Another address',
                        },
                    status_codes=[str(status.HTTP_200_OK)],
                    response_only=True
                )
            ]
            )
    def get(self, request, id):
        lib = self.get_object(id)
        serialiser = LibrarySerialiser(lib)
        return Response(serialiser.data, status=status.HTTP_200_OK)
    
    @extend_schema(
            summary='Update information about a library',
            responses={
                status.HTTP_200_OK: LibrarySerialiser,
                status.HTTP_400_BAD_REQUEST: DummyDetailAndStatusSerializer,
                status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                    response=None,
                    description='Описание 500 ответа'
                    )
            },
            examples=[
                OpenApiExample(
                    'Put example',
                    description='Test update of a library',
                    value={
                            'id': 2,
                            'address': 'Another address',
                        },
                    status_codes=[str(status.HTTP_200_OK)],
                    response_only=True
                )
            ]
            )
    def put(self, request, id):
        lib = self.get_object(id)
        serializer = LibrarySerialiser(lib, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
            summary='Delete library',
            responses={
                status.HTTP_204_NO_CONTENT: DummyDetailAndStatusSerializer,
                status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                    response=None,
                    description='Описание 500 ответа'
                    )
            },
            )
    def delete(self, request, id):
        lib = self.get_object(id)
        lib.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=['Library'])
@extend_schema_view()
class LibraryBooks(APIView):
    @extend_schema(
            summary='Get list of all books in a library',
            responses={
                status.HTTP_200_OK: BookSerialiser,
                status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                    response=None,
                    description='Описание 500 ответа'
                    )
            },
            examples=[
                OpenApiExample(
                    'Get example',
                    description='Get list of all books in a library example',
                    value=[
                        {
                            "name": "1984",
                            "author": "Dj. Orwell",
                            "creation_date": "2024-09-10",
                            "library": 1,
                            "file": 'null'
                        },
                        {
                            "name": "Absolute weapon",
                            "author": "Robert Shakley",
                            "creation_date": "2024-09-03",
                            "library": 1,
                            "file": 'null'
                        }
                    ],
                    status_codes=[str(status.HTTP_200_OK)],
                    response_only=True
                )
            ]
            )
    def get(self, request, id):
        lib = Library.objects.get(id=id)
        books = Book.objects.filter(library=lib)
        return Response(BookSerialiser(books, many=True).data, status=status.HTTP_200_OK)


@extend_schema(tags=['Book'])
@extend_schema_view()
class BookList(APIView):
    @extend_schema(
            summary='Get list of all books',
            responses={
                status.HTTP_200_OK: BookSerialiser,
                status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                    response=None,
                    description='Описание 500 ответа'
                    )
            },
            examples=[
                OpenApiExample(
                    'Get example',
                    description='Get list of all books example',
                    value=[
                        {
                            "name": "1984",
                            "author": "Dj. Orwell",
                            "creation_date": "2024-09-10",
                            "library": 1,
                            "file": 'null'
                        },
                        {
                            "name": "451 degrees Farengheit",
                            "author": "Ray Bradberry",
                            "creation_date": "2024-09-11",
                            "library": 2,
                            "file": 'null'
                        },
                        {
                            "name": "Absolute weapon",
                            "author": "Robert Shakley",
                            "creation_date": "2024-09-03",
                            "library": 1,
                            "file": 'null'
                        },
                        {
                            "name": "Ticket to Tranay",
                            "author": "Robert Shakley",
                            "creation_date": "2024-09-14",
                            "library": 1,
                            "file": 'null'
                        },
                        {
                            "name": "The last challenge",
                            "author": "Robert Shakley",
                            "creation_date": "2024-09-14",
                            "library": 1,
                            "file": 'null'
                        }
                    ],
                    status_codes=[str(status.HTTP_200_OK)],
                    response_only=True
                )
            ],
            parameters=[
                OpenApiParameter(
                    name='author',
                    location=OpenApiParameter.QUERY,
                    description='Author to filter by',
                    required=False,
                    type=str
                ),
                OpenApiParameter(
                    name='creation_date',
                    location=OpenApiParameter.QUERY,
                    description='Creation date to filter by',
                    required=False,
                    type=str
                ),
                OpenApiParameter(
                    name='name',
                    location=OpenApiParameter.QUERY,
                    description='Name to filter by',
                    required=False,
                    type=str
                )
            ]
            )
    def get(self, request, format=None):
        if len(request.GET) >= 0:
            books = Book.objects.filter(**request.GET.dict())
            serializer = BookSerialiser(books, many=True)
        else:
            books = Book.objects.all()
            serializer = BookSerialiser(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
            summary='Add a new book',
            responses={
                status.HTTP_201_CREATED: BookSerialiser,
                status.HTTP_400_BAD_REQUEST: DummyDetailAndStatusSerializer,
                status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                    response=None,
                    description='Описание 500 ответа'
                    )
            },
            examples=[
                OpenApiExample(
                    'Post example',
                    description='Both post and response example',
                    value={
                            "name": "The last challenge",
                            "author": "Robert Shakley",
                            "creation_date": "2024-09-14",
                            "library": 1,
                            "file": 'null'
                        },
                    status_codes=[str(status.HTTP_201_CREATED)]
                )
            ]
        )
    def post(self, request, format=None):
        serializer = BookSerialiser(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Book'])
@extend_schema_view()
class BookView(APIView):
    def get_object(self, id):
        try:
            return Book.objects.get(id=id)
        except Book.DoesNotExist:
            raise Http404
    
    @extend_schema(
            summary='Get information about a book',
            responses={
                status.HTTP_200_OK: BookSerialiser,
                status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                    response=None,
                    description='Описание 500 ответа'
                    )
            },
            examples=[
                OpenApiExample(
                    'Get example',
                    description='Test view of a book',
                    value={
                            "name": "The last challenge",
                            "author": "Robert Shakley",
                            "creation_date": "2024-09-14",
                            "library": 1,
                            "file": 'null'
                        },
                    status_codes=[str(status.HTTP_200_OK)],
                    response_only=True
                )
            ]
            )
    def get(self, request, id):
        book = self.get_object(id)
        serialiser = BookSerialiser(book)
        return Response(serialiser.data, status=status.HTTP_200_OK)
    
    @extend_schema(
            summary='Update information about a book',
            responses={
                status.HTTP_200_OK: BookSerialiser,
                status.HTTP_400_BAD_REQUEST: DummyDetailAndStatusSerializer,
                status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                    response=None,
                    description='Описание 500 ответа'
                    )
            },
            examples=[
                OpenApiExample(
                    'Put example',
                    description='Test update of a book',
                    value={
                            "name": "The last challenge",
                            "author": "Robert Shakley",
                            "creation_date": "2024-09-14",
                            "library": 1,
                            "file": 'null'
                        },
                    status_codes=[str(status.HTTP_200_OK)],
                    response_only=True
                )
            ]
            )
    def put(self, request, id):
        book = self.get_object(id)
        serializer = BookSerialiser(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
            summary='Delete book',
            responses={
                status.HTTP_204_NO_CONTENT: DummyDetailAndStatusSerializer,
                status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                    response=None,
                    description='Описание 500 ответа'
                    )
            },
            )
    def delete(self, request, id):
        book = self.get_object(id)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)