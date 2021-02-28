# Generated by Django 3.1.5 on 2021-02-13 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogbooks', '0008_auto_20210213_1307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookinstance',
            name='book_status',
            field=models.CharField(blank=True, choices=[('НН', 'Нет в наличии'), ('А', 'В аренде'), ('Н', 'В наличии'), ('Р', 'В резерве')], default='Н', help_text='Наличие книги', max_length=3),
        ),
    ]
