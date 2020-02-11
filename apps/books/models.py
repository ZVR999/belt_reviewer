# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ..authors.models import Author
# Create your models here.

class BookManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['book_title']) < 2:
            errors['book_title'] = 'Book Title field must be at least 2 characters'
        if postData['new_author']:
            if len(postData['new_author']) < 2:
                errors['new_author'] = 'New Author field must be at least 2 characters'
        if len(postData['review']) < 2:
            errors['review'] = 'Review field must be at least 2 characters long'
        if not postData['rating']:
            errors['rating'] = 'There is no rating selected'
        return errors


class Book(models.Model):
    name = models.CharField(max_length=255)
    author = models.ForeignKey(Author, related_name='books',on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    objects = BookManager()