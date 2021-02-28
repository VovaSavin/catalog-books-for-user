from django.test import TestCase
from .models import Author


class AuthorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Author.objects.create(name='Vovos', surname='Vavas')

    def test_name_label(self):
        author = Author.objects.get(id=1)
        name_label = author._meta.get_field('name').verbose_name
        self.assertEqual(name_label, 'Имя')

    def test_surname_label(self):
        author = Author.objects.get(id=1)
        surname_label = author._meta.get_field('surname').verbose_name
        self.assertEqual(surname_label, 'Фамилия')

    def test_name_lenght(self):
        author = Author.objects.get(id=1)
        lenght = author._meta.get_field('name').max_length
        self.assertEqual(lenght, 100)

    def test_surname_lenght(self):
        author = Author.objects.get(id=1)
        lenght = author._meta.get_field('surname').max_length
        self.assertEqual(lenght, 100)

    def test_date_birth_label(self):
        author = Author.objects.get(id=1)
        birth_label = author._meta.get_field('date_birth').verbose_name
        self.assertEqual(birth_label, 'Дата рождения')

    def test_date_death_label(self):
        author = Author.objects.get(id=1)
        death_label = author._meta.get_field('date_death').verbose_name
        self.assertEqual(death_label, 'Дата смерти')

    def test_str_author(self):
        author = Author.objects.get(id=1)
        full_name = f'{author.surname} {author.name}'
        self.assertEqual(full_name, str(author))
    
    def test_url_specified_author(self):
        author = Author.objects.get(id=1)
        self.assertEqual(author.get_absolute_url(), '/catalog/author/1') # get_absolute_url() вызываем, иначе исключение будет