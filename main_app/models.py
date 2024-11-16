from django.db import models


class Book(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    year = models.IntegerField()
    cover = models.ImageField(upload_to='covers', null=True, blank=True)
    author = models.ForeignKey('Author', on_delete=models.CASCADE, null=True, blank=True)
    genres = models.ManyToManyField('Genre')

    def __str__(self):
        return self.name

from django.contrib.auth.models import User

class Cart(models.Model):
    items = models.ManyToManyField('CartItem')
    customer = models.ForeignKey(User, on_delete=models.CASCADE)


class CartItem(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)


class Author(models.Model):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
