from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User
from django_cryptography.fields import encrypt

class Note(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    note_header = models.CharField(max_length=30, blank=True, null=True)
    note_text = models.CharField(max_length=300)
    note_date = models.DateTimeField('note date')

    def __str__(self):
        return self.note_text

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    username = models.CharField('username', max_length=50)
    address = models.CharField('address', max_length=200, null=True)