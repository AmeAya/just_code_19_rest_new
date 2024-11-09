from django.db import models


class Book(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    year = models.IntegerField()
    author = models.ForeignKey('Author', on_delete=models.CASCADE, null=True, blank=True)
    genres = models.ManyToManyField('Genre')

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
