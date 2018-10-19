from django.test import TestCase
from .models import Publisher, Author, Book, Category


class TestSafeModel(TestCase):

    def test_related_fields(self):
        self.assertEqual(len(Author.related_fields()), 1)
