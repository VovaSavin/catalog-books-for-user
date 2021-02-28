from django.contrib import admin
from .models import (
    Books,
    BookInstance,
    Genre,
    Author,
    LanguageBook,
)

# Register your models here.

admin.site.register(Genre)
admin.site.register(LanguageBook)

class BooksInline(admin.TabularInline):
    '''Указываем имя и метод размещения полей ввода одной модели в другую на админ-панели'''
    # В данном примере горизонтальное размещение

    extra = 0 # Доп экземпляры для заполнения - убираем их на хрен!!!
    model = Books


class AuthorAdmin(admin.ModelAdmin):
    '''Переопределяем поля для админ-панели'''

    list_display = ('name', 'surname', 'date_birth', 'date_death')
    fields = [('name','surname'), ('date_birth', 'date_death')]
    inlines = [BooksInline]

class BookInstanceInline(admin.TabularInline):
    '''Указываем имя и метод размещения полей ввода одной модели в другую на админ-панели'''
    # В данном примере горизонтальное размещение

    extra = 0 # Доп экземпляры для заполнения - убираем их на хрен!!!
    model = BookInstance


@admin.register(Books)
class BooksAdmin(admin.ModelAdmin):
    '''Переопределяем поля для админ-панели'''

    list_display = ('title', 'author', 'genre_display')
    list_filter = ('genre', 'language')
    inlines = [BookInstanceInline]

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    '''Переопределяем поля для админ-панели'''

    list_display = ('book', 'book_status', 'date_back', 'uniq_id')
    list_filter = ('book_status', 'date_back', 'book')
    fieldsets = (
        (
            'Общая информация',
            {'fields': ('uniq_id', 'book', 'imprint')},
        ),
        (
            'Детальный статус',
            {'fields': ('date_back', 'book_status', 'debtor')},
        ),
    )

admin.site.register(Author, AuthorAdmin)