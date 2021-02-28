import datetime

from django.test import TestCase
from .forms import BookRenewForm


class BookRenewFormTest(TestCase):
    def test_new_date_back_label(self):
        form = BookRenewForm()
        self.assertTrue(form.fields['new_date_back'].label == 'Новая дата:')

    def test_new_date_back_help_text(self):
        form = BookRenewForm()
        self.assertEqual(form.fields['new_date_back'].help_text, 'От сегодня и на 3 недели вперёд(max)')
    
    def test_new_date_back_tomorrow_date(self):
        date = datetime.date.today() - datetime.timedelta(days=1)
        form = BookRenewForm(data={'new_date_back': date})
        self.assertFalse(form.is_valid())

    def test_new_date_back_max_plus_1_day(self):
        date = datetime.date.today() + datetime.timedelta(weeks=3) + datetime.timedelta(days=1)
        form = BookRenewForm(data={'new_date_back': date})
        self.assertFalse(form.is_valid())
    
    def test_new_date_back_today(self):
        date = datetime.date.today()
        form = BookRenewForm(data={'new_date_back': date})
        self.assertTrue(form.is_valid())
    
    def test_new_date_back_max_date(self):
        date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = BookRenewForm(data={'new_date_back': date})
        self.assertTrue(form.is_valid())