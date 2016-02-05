from django.db import models

class Book(models.Model):
    title=models.CharField(max_length=100)
    id=models.IntegerField(primary_key=True)

class Author(models.Model):
    name=models.CharField(max_length=70)
    id=models.IntegerField(primary_key=True)

class BookAuthor(models.Model):
    book_id=models.ForeignKey(Book)
    author_id=models.ForeignKey(Author)
