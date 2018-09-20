# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from ..authors.models import Author
from ..reviews.models import Review
from ..users.models import User
from .models import Book
from django.contrib import messages
# Create your views here.


def index(request):
    context = {
        'reviews': Review.objects.order_by('-created_at')[:3],
        'books': Book.objects.all()
    }

    return render(request, 'books/index.html', context)


def add(request):
    context = {
        'authors': Author.objects.all()
    }
    return render(request, 'books/add.html', context)


def create(request):
    reviewErrors = Review.objects.basic_validator(request.POST)
    bookErrors = Book.objects.basic_validator(request.POST)

    if len(reviewErrors):
        for tag, error in reviewErrors.iteritems():
            messages.error(request, error, extra_tags=tag)

    if len(bookErrors):
        for tag, error in bookErrors.iteritems():
            messages.error(request, error, extra_tags=tag)

        if not Author.objects.all():
            messages.error(request, 'There are no authors. Please create one')

        return redirect('/books/add')

    # Check if there was a new author inputted
    if request.POST['new_author']:
        request.session['author'] = request.POST['new_author']
    else:
        request.session['author'] = request.POST['author']

    author = request.session['author']
    review = request.POST['review']
    rating = request.POST['rating']
    book = request.POST['book_title']

    # Check to make sure book is not already in the DB
    if not Book.objects.filter(name=book):
        request.session['book'] = book
        # Check if the new author is already in the DB
        if not Author.objects.filter(name=author):
            Author.objects.create(name=author)
            author_to_add = Author.objects.get(name=author)
        else:
            author_to_add = Author.objects.get(name=author)
    else:
        messages.error(request, 'This book already exists')
        return redirect('/books/add')

    # Create book
    Book.objects.create(name=book, author=author_to_add)
    book_to_add = Book.objects.get(name=book)

    # Create Review
    user_to_add = User.objects.get(alias=request.session['alias'])

    Review.objects.create(rating=rating, review=review,
                          book=book_to_add, user=user_to_add)

    return redirect('/books/'+str(book_to_add.id))


def show(request, book_id):
    context = {
        'book': Book.objects.get(id=book_id),
        'reviews': Review.objects.filter(book=Book.objects.get(id=book_id)).order_by('-created_at')
    }
    
    return render(request, 'books/book.html', context)
