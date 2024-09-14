from django.db import models
import django
import datetime

# Create your models here.
class Library(models.Model):
    address = models.CharField(max_length=100)


class Book(models.Model):
    name = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    file = models.FileField(blank=True)  # TODO [задача] сделай здесь именно поле с файлом --OK
    creation_date = models.DateField(default=django.utils.timezone.now)
    library = models.ForeignKey(Library, on_delete=models.CASCADE)