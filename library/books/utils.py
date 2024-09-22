from .models import Library
from django.http import Http404


class LibraryMixin:
    def get_object(self, id):
        try:
            return Library.objects.get(id=id)
        except Library.DoesNotExist:
            raise Http404