# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponseRedirect
from django.shortcuts import render
from ..reviews.models import Review
from ..users.models import User
from ..books.models import Book
from django.contrib import messages
# Create your views here.


def index(request):
    pass


def create(request):
    book = Book.objects.get(id=request.POST['book_id'])
    
    errors = Review.objects.basic_validator(request.POST)

    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)

        return HttpResponseRedirect('/books/'+str(request.POST['book_id']))
    
    rating = request.POST['rating']
    review = request.POST['review']
    book_to_add = book
    user_to_add = User.objects.get(alias=request.session['alias'])
    Review.objects.create(rating=rating, review=review,
                          book=book_to_add, user=user_to_add)
    return HttpResponseRedirect('/books/'+str(request.POST['book_id']))

def delete(request, review_id):
    review = Review.objects.get(id=review_id)
    book_id = review.book.id
    review.delete()

    return HttpResponseRedirect('/books/'+str(book_id))
