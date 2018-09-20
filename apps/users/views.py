# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from .models import User
from ..reviews.models import Review
from ..books.models import Book
import bcrypt
from django.contrib import messages
# Create your views here.

# Create a User
def create(request):
    errors = User.objects.basic_validator(request.POST)
    hashed_pw = bcrypt.hashpw(
        request.POST['password'].encode(), bcrypt.gensalt())

    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)

        return redirect('/')

    user_exists = User.objects.filter(email=request.POST['email'])
    if user_exists:
        messages.error(request, 'This email is already in use')

        return redirect('/')
    else:
        request.session['alias'] = request.POST['alias']
        name = request.POST['name']
        alias = request.POST['alias']
        email = request.POST['email']

        User.objects.create(name=name, alias=alias,
                            email=email, password=hashed_pw)

    return redirect('/books')

# Login a User
def login(request):
    user_exists = User.objects.filter(email=request.POST['email'])
    if user_exists:
        db_password = str(user_exists[0].password)
        if bcrypt.checkpw(str(request.POST['password']), db_password.encode()):
            request.session['alias'] = user_exists[0].alias
            return redirect('/books')
        else:
            messages.error(request, 'Invalid email or password')
    else:
        messages.error(request, 'Invalid email or password')

    return redirect('/')


def show(request, user_id):
    user = User.objects.get(id=user_id)
    Review.objects.filter()
    context = {
        'user': User.objects.get(id=user_id),
        'books': Review.objects.raw('SELECT DISTINCT "books_Book"."id", "books_Book"."name" FROM reviews_Review JOIN books_Book ON "reviews_Review"."book_id"="books_Book"."id" WHERE "reviews_Review"."user_id"='+str(user.id)+';')
    }
    request.session['total'] = Review.objects.filter(user=User.objects.filter(id=user_id)).count()
    return render(request, 'users/user.html', context)

def logout(request):
    request.session['alias'] = 'Please Login or Register'
    return redirect('/')
