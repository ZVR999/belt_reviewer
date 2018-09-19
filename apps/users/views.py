# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from ..users.models import User
import bcrypt
from django.contrib import messages
# Create your views here.

# Create a User
def create(request):
    request.session['user_id'] = 1
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


def logout(request):
    request.session['alias'] = 'Please Login or Register'
    return redirect('/')
