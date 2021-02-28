from django.db import models
from django.urls import reverse
import uuid
from django.contrib.auth.models import User
from datetime import date

# Create your models here.


class Author(models.Model):
    '''Класс для создание в БД информации об авторе и егo книгах'''

    name = models.CharField(max_length=100, verbose_name='Имя')
    surname = models.CharField(max_length=100, verbose_name='Фамилия')
    date_birth = models.DateField(
        null=True, blank=True, verbose_name='Дата рождения')
    date_death = models.DateField(
        null=True, blank=True, verbose_name='Дата смерти')

    def get_absolute_url(self):
        return reverse('author_info', args=[str(self.id)])

    def __str__(self):
        return f'{self.surname} {self.name}'

    class Meta:
        ordering = ['surname', 'name']
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class LanguageBook(models.Model):
    '''Класс для создания табл в БД для книг на разных языках'''

    language = models.CharField(
        max_length=100, help_text='Выбери язык книги', verbose_name='Язык')

    def __str__(self):
        return f'{self.language}'

    class Meta:
        ordering = ['language']
        verbose_name = 'Язык'
        verbose_name_plural = 'Языки'


class Genre(models.Model):
    '''Класс для создания табл с жанрами книг в БД'''

    name_genre = models.CharField(
        max_length=100, help_text='Выбери жанр книги', verbose_name='Жанр')

    def __str__(self):
        return f'Жанр: {self.name_genre}'

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Books(models.Model):
    '''Клас для таблиц описания книг в БД'''

    title = models.CharField(max_length=100, verbose_name='Название книги')
    author = models.ForeignKey(
        Author, on_delete=models.SET_NULL, null=True, verbose_name='Автор')
    language = models.ManyToManyField(LanguageBook, verbose_name='Язык')
    genre = models.ManyToManyField(Genre, verbose_name='Жанр')
    summary = models.TextField(
        help_text='Описание книги', verbose_name='Краткое описание')
    isbn = models.CharField(
        'ISBN',
        max_length=13,
        unique=True,
        help_text='<a href="https://www.isbn-international.org/content/what-isbn">ISBN номер</a>',
        null=True,
        blank=True,
    )

    def genre_display(self):
        '''Определяем связанные с Books через M2M поля для отображения их в админ-панели'''
        # Принцип работы для M2M

        return ','.join(genre.name_genre for genre in self.genre.all()[:3])

    genre_display.short_description = 'Жанр'

    def __str__(self):
        return f'Книга: {self.title}'

    def get_absolute_url(self):
        return reverse('books-detail', args=[str(self.id)])

    class Meta:
        permissions = (("create_book_bystaff", "Create new book"),)
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'


class BookInstance(models.Model):
    '''Таблица в БД с информацией о статусе книги'''

    uniq_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, help_text='Уникальный идентификатор книги', verbose_name='Идентификатор',
    )
    book = models.ForeignKey(
        Books, on_delete=models.RESTRICT, verbose_name='Книга')
    imprint = models.CharField(max_length=100)
    date_back = models.DateField(null=True, blank=True)

    book_variant = (
        ('НН', 'Нет в наличии'),
        ('А', 'В аренде'),
        ('Н', 'В наличии'),
        ('Р', 'В резерве'),
    )
    book_status = models.CharField(
        max_length=3,
        choices=book_variant,
        blank=True,
        default='Н',
        help_text='Наличие книги',
        verbose_name='Текущий статус',
    )
    debtor = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True)

    @property
    def is_overdue(self):
        '''Проверяем: прострочена ли книга?'''
        if self.date_back and date.today() > self.date_back:
            return True
        return False

    def __str__(self):
        return f'{self.uniq_id} - {self.book.title}'

    class Meta:
        permissions = (("can_mark_returned", "Set book as returned"),)
        ordering = ['date_back']
        verbose_name = 'Экземпляр книги'
        verbose_name_plural = 'Экземпляры книг'
