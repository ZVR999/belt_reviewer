# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

# Create your views here.

def index(request):
    return render(request, 'books/index.html')

def new(request):
    return render(request, 'books/new.html')

def create(request):
    return redirect('/books')

def show(request,book_id):
    return render(request, 'books/book.html')