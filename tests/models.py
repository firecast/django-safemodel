from django.db import models

from safemodel.models import SafeModel
from safemodel import SOFT_DELETE, SOFT_DELETE_CASCADE, NO_DELETE


class Publisher(SafeModel):
    _safe_policy = SOFT_DELETE_CASCADE
    _safe_relation_classes = ['Author']

    name = models.CharField(max_length=100)


class Author(SafeModel):
    _safe_policy = SOFT_DELETE_CASCADE
    _safe_relation_classes = ['Book']

    name = models.CharField(max_length=200)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, related_name='authors')


class Category(SafeModel):
    _safe_policy = NO_DELETE
    name = models.CharField(max_length=100)


class Book(SafeModel):
    _safe_policy = SOFT_DELETE

    name = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    categories = models.ManyToManyField(Category, related_name='books')
