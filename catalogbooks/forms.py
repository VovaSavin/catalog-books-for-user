import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class BookRenewForm(forms.Form):
    '''Форма для установки и изменения даты возврата книги'''

    new_date_back = forms.DateField(
        help_text='От сегодня и на 3 недели вперёд(max)', label='Новая дата:')

    def clean_new_date_back(self):
        '''Проверяем корректность заполнения форм'''

        data = self.cleaned_data['new_date_back']

        if data < datetime.date.today():
            raise ValidationError(_('Нельзя ставить прошедшую дату!'))
        if data > datetime.date.today() + datetime.timedelta(weeks=3):
            raise ValidationError(
                _('Нельзя ставить дату больше чем на 3 недели вперёд!'))
        return data
