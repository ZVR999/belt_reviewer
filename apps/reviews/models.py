# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ..books.models import Book
from ..users.models import User
# Create your models here.

class ReviewManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if not postData['rating']:
            errors['rating'] = 'Please select a rating'
        if len(postData['review']) < 2:
            errors['review'] = 'Review must be long than 2 characters'
        return errors


class Review(models.Model):
    rating = models.IntegerField()
    review = models.CharField(max_length=255)
    book = models.ForeignKey(Book, related_name='reviews')
    user = models.ForeignKey(User, related_name='reviews')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ReviewManager()
