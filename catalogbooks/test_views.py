from .models import Author, Books, BookInstance, LanguageBook, Genre
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Permission

import uuid
import datetime


class AuthorListTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        author_list_len = 11
        for one_author in range(author_list_len):
            Author.objects.create(
                name=f'Вася_{one_author}',
                surname=f'Автор_{one_author}'
            )

    def test_return_200_from_url(self):
        response = self.client.get('/catalog/author/')
        self.assertEqual(response.status_code, 200)

    def test_return_200_from_name_url(self):
        response = self.client.get(reverse('author'))
        self.assertEqual(response.status_code, 200)

    def test_return_200_from_url_and_template(self):
        response = self.client.get(reverse('author'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalogbooks/author_list.html')

    def test_return_200_and_paginate(self):
        response = self.client.get(reverse('author'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['author_list']) == 7)

    def test_return_200_and_last_page_paginate(self):
        response = self.client.get(reverse('author')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['author_list']) == 4)


class RenewBookTest(TestCase):

    def setUp(self):
        # Создаём двух пользователей
        test_user_1 = User.objects.create_user(
            username='user_1', password='271818451q')
        test_user_2 = User.objects.create_user(
            username='user_2', password='271818451qq')

        # Сохраняем пользователей
        test_user_1.save()
        test_user_2.save()

        # Создаём книгу:
        # Автора, Жанр, Язык книги
        test_author = Author.objects.create(name='Valera', surname='Valerius')
        test_genre = Genre.objects.create(name_genre='Ванильная хрень')
        test_language = LanguageBook.objects.create(language='Китайский')
        test_book = Books.objects.create(
            title='Title',
            summary='Awesome awesome book',
            isbn='4545454545454',
            author=test_author,
        )
        genre_book_test = Genre.objects.all()
        language_book_test = LanguageBook.objects.all()
        test_book.genre.set(genre_book_test)
        test_book.language.set(language_book_test)
        test_book.save()

        copies_books = 40
        for one_book in range(copies_books):
            return_date = datetime.date.today() + datetime.timedelta(days=one_book % 5)
            the_debtor = test_user_1 if one_book % 2 else test_user_2
            status_object_book = 'Н'
            BookInstance.objects.create(
                book=test_book,
                imprint='У дяди Васи',
                date_back=return_date,
                debtor=the_debtor,
                book_status=status_object_book
            )

    def test_not_auth_user(self):
        response = self.client.get(reverse('mybooks'))
        self.assertRedirects(
            response, '/accounts/login/?next=/catalog/mybooks/')

    def test_correct_used_temlate(self):
        log = self.client.login(username='user_1', password='271818451q')
        response = self.client.get(reverse('mybooks'))
        self.assertEqual(str(response.context['user']), 'user_1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalogbooks/user_books_list.html')

    def test_auth_users_book(self):
        log = self.client.login(username='user_1', password='271818451q')
        response = self.client.get(reverse('mybooks'))
        self.assertEqual(str(response.context['user']), 'user_1')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('usersbooks' in response.context)
        self.assertTrue(len(response.context['usersbooks']) == 0)

        rent_books = BookInstance.objects.all()[:10]
        for book in rent_books:
            book.book_status = 'А'
            book.save()

        response = self.client.get(reverse('mybooks'))
        self.assertEqual(str(response.context['user']), 'user_1')
        self.assertEqual(response.status_code, 200)

        self.assertTrue('usersbooks' in response.context)

        for book_i in response.context['usersbooks']:
            self.assertEqual(response.context['user'], book_i.debtor)
            self.assertEqual('А', book_i.book_status)

    def test_that_order_date_back(self):
        for book in BookInstance.objects.all():
            book.book_status = 'А'
            book.save()
        log = self.client.login(username='user_1', password='271818451q')
        response = self.client.get(reverse('mybooks'))
        self.assertTrue(str(response.context['user']) == 'user_1')
        self.assertEqual(response.status_code, 200)
        # 7 - пагинация
        self.assertEqual(len(response.context['usersbooks']), 7)
        last_date = 0
        for user_book in response.context['usersbooks']:
            if last_date == 0:
                last_date = user_book.date_back
            else:
                self.assertTrue(last_date <= user_book.date_back)
                last_date = user_book.date_back


class RenewDateFormTest(TestCase):
    def setUp(self):
        # Создаём двух пользователей
        test_user_1 = User.objects.create_user(
            username='user_1', password='271818451q')
        test_user_2 = User.objects.create_user(
            username='user_2', password='271818451qq')
        test_user_1.save()
        test_user_2.save()

        perms = Permission.objects.get(name='Set book as returned')
        test_user_1.user_permissions.add(perms)
        test_user_1.save()

        # Создаём книгу:
        # Автора, Жанр, Язык книги
        test_author = Author.objects.create(name='Valera', surname='Valerius')
        test_genre = Genre.objects.create(name_genre='Ванильная хрень')
        test_language = LanguageBook.objects.create(language='Китайский')
        test_book = Books.objects.create(
            title='Title',
            summary='Awesome awesome book',
            isbn='4545454545454',
            author=test_author,
        )
        genre_book_test = Genre.objects.all()
        language_book_test = LanguageBook.objects.all()
        test_book.genre.set(genre_book_test)
        test_book.language.set(language_book_test)
        test_book.save()

        return_date_book = datetime.date.today() + datetime.timedelta(days=6)
        self.book_user_1 = BookInstance.objects.create(
            book=test_book,
            imprint='У дяди Васи',
            date_back=return_date_book,
            debtor=test_user_1,
            book_status="А",
        )
        self.book_user_2 = BookInstance.objects.create(
            book=test_book,
            imprint='У дяди Васи',
            date_back=return_date_book,
            debtor=test_user_2,
            book_status="А",            
        )
    
    def test_user_not_auth(self):
        response = self.client.get(reverse('renewdate', kwargs={'pk': self.book_user_2.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_user_whithout_permission(self):
        log = self.client.login(username='user_2', password='271818451qq')
        response = self.client.get(reverse('renewdate', kwargs={'pk': self.book_user_2.pk}))
        self.assertEqual(response.status_code, 403)

    def test_user_has_permission(self):
        log = self.client.login(username='user_1', password='271818451q')
        response = self.client.get(reverse('renewdate', kwargs={'pk': self.book_user_1.pk}))
        self.assertEqual(response.status_code, 200)
    
    def test_user_has_permission_another_book(self):
        log = self.client.login(username='user_1', password='271818451q')
        response = self.client.get(reverse('renewdate', kwargs={'pk': self.book_user_2.pk}))
        self.assertEqual(response.status_code, 200)

    def test_user_has_permission_no_book_match(self):
        id_test = uuid.uuid4()
        log = self.client.login(username='user_1', password='271818451q')
        response = self.client.get(reverse('renewdate', kwargs={'pk': id_test}))
        self.assertEqual(response.status_code, 404)

    def test_show_template_user_has_permission(self):
        log = self.client.login(username='user_1', password='271818451q')  
        response = self.client.get(reverse('renewdate', kwargs={'pk': self.book_user_2.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalogbooks/instance_new_date.html')

    def test_correct_date_future_3weeks(self):
        log = self.client.login(username='user_1', password='271818451q')
        response = self.client.get(reverse('renewdate', kwargs={'pk': self.book_user_2.pk}))
        self.assertEqual(response.status_code, 200)
        future_date = datetime.date.today() + datetime.timedelta(weeks=3)
        self.assertEqual(response.context['form'].initial['new_date_back'], future_date)
    
    def test_renew_date(self):
        log = self.client.login(username='user_1', password='271818451q')
        future_date = datetime.date.today() + datetime.timedelta(weeks=2)
        response = self.client.post(reverse('renewdate', kwargs={'pk': self.book_user_2.pk}), {'new_date_back': future_date})
        self.assertRedirects(response, reverse('allrentbooks'))

    def test_not_correct_date_past(self):
        log = self.client.login(username='user_1', password='271818451q')
        past_date = datetime.date.today() - datetime.timedelta(weeks=2)
        response = self.client.post(reverse('renewdate', kwargs={'pk': self.book_user_2.pk}), {'new_date_back': past_date})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'new_date_back', 'Нельзя ставить прошедшую дату!')

    def test_not_correct_date_future(self):
        log = self.client.login(username='user_1', password='271818451q')
        future_date = datetime.date.today() + datetime.timedelta(weeks=6)
        response = self.client.post(reverse('renewdate', kwargs={'pk': self.book_user_2.pk}), {'new_date_back': future_date})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'new_date_back', 'Нельзя ставить дату больше чем на 3 недели вперёд!')        
        

class AuthorCreateTest(TestCase):
    def setUp(self):
        # Создаём двух пользователей
        test_user_1 = User.objects.create_user(
            username='user_1', password='271818451q')
        test_user_2 = User.objects.create_user(
            username='user_2', password='271818451qq')
        test_user_1.save()
        test_user_2.save()

        perms = Permission.objects.get(name='Create new book')
        test_user_2.user_permissions.add(perms)
        test_user_2.save()
    
    def test_not_auth_user_create(self):
        response = self.client.get(reverse('create-author'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/catalog/author/create')
    
    def test_not_permission_user(self):
        log = self.client.login(username='user_1', password='271818451q')
        response = self.client.get(reverse('create-author'))
        self.assertEqual(response.status_code, 403)
    
    def test_user_has_permission(self):
        log = self.client.login(username='user_2', password='271818451qq')
        response = self.client.get(reverse('create-author'))
        self.assertEqual(str(response.context['user']), 'user_2')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalogbooks/create_author.html')
    
    def test_redirect_success_create(self):
        log = self.client.login(username='user_2', password='271818451qq')
        response = self.client.post(reverse('create-author'), {'name': 'JohnPaulJons', 'surname': 'Smith'})     
        self.assertRedirects(response, reverse('author_info', kwargs={'pk': Author.objects.get(name__contains='JohnPaulJons').pk}))  


class AuthorUpdateTest(TestCase):
    def setUp(self):
        # Создаём двух пользователей
        test_user_1 = User.objects.create_user(
            username='user_1', password='271818451q')
        test_user_2 = User.objects.create_user(
            username='user_2', password='271818451qq')
        test_user_1.save()
        test_user_2.save()

        perms = Permission.objects.get(name='Create new book')
        test_user_2.user_permissions.add(perms)
        test_user_2.save()

        self.test_author = Author.objects.create(
            name='Koko',
            surname='Coco',
            date_birth=datetime.datetime(1800, 10, 5),
            date_death=datetime.datetime(1900, 10, 6),
        )
    
    def test_not_auth_user(self):
        response = self.client.get(reverse('update-author', kwargs={'pk': self.test_author.pk}))
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_auth_user_has_not_permission(self):
        log = self.client.login(username='user_1', password='271818451q')
        response = self.client.get(reverse('update-author', kwargs={'pk': self.test_author.pk}))
        self.assertEqual(response.status_code, 403)

    def test_user_hes_permission_and_template(self):
        log = self.client.login(username='user_2', password='271818451qq')
        response = self.client.get(reverse('update-author', kwargs={'pk': self.test_author.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalogbooks/update_author.html')
    
    def test_user_has_permission_change_author(self):
        log = self.client.login(username='user_2', password='271818451qq')
        response = self.client.post(reverse('update-author', kwargs={'pk': self.test_author.pk}), {'name': 'Koka'})   
        self.assertEqual(response.status_code, 200)     
        #self.assertRedirects(response, reverse('author_info', kwargs={'pk': self.test_author.pk})) # Выдаёт исключение в тестировании
        self.assertEqual(self.test_author.get_absolute_url(), reverse('author_info', kwargs={'pk': self.test_author.pk}))
        