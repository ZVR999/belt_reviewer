# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re
EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
# Create your models here.


class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['name']) < 2:
            errors['name'] = 'Length of Name must be at least 2 characters'
        if len(postData['alias']) < 2:
            errors['alias'] = 'Length of Alias must be at least 2 characters'
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'Email is not valid'
        if len(postData['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters long'
        if postData['confirm_password'] != postData['password']:
            errors['confirm_password'] = 'Confirm Password does not match Password'
        return errors


class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    objects = UserManager()
