#coding=utf8
from django.db import models

# Create your models here.
class Author(models.Model):
    AuthorID = models.IntegerField(primary_key = True)
    Name = models.CharField(max_length = 20, unique=True)
    Age = models.CharField(max_length = 10)
    Country = models.CharField(max_length = 20)

    def __unicode__(self):
        return self.Name

class Book(models.Model):
    ISBN = models.IntegerField(primary_key = True)
    AuthorID = models.ForeignKey(Author)
    Publisher = models.CharField(max_length = 30)
    PublishDate = models.CharField(max_length = 20)
    Price = models.CharField(max_length = 10)

    def __unicode__(self):
        return self.Title


