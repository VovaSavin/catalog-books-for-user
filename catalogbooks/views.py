import datetime

from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import (
    Author,
    Books,
    BookInstance,
    Genre,
    LanguageBook,
)
from django.views.generic import (
    ListView,
    DetailView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import BookRenewForm
# Create your views here.


def main_foo(request):
    '''Главная страница сайта'''

    num_books = Books.objects.all().count()
    num_instance_books = BookInstance.objects.all().count()
    num_author = Author.objects.all().count()
    num_instance_books_n = BookInstance.objects.filter(
        book_status__exact='Н').count()
    num_genre = Genre.objects.all().count()
    num_language = LanguageBook.objects.all().count()
    num_visit = request.session.get('num_visit', 1)
    request.session['num_visit'] = num_visit + 1
    context = {
        'num_books': num_books,
        'num_instance_books': num_instance_books,
        'num_author': num_author,
        'num_instance_books_n': num_instance_books_n,
        'num_genre': num_genre,
        'num_language': num_language,
        'title': 'Главная страница',
        'num_visit': num_visit,
    }
    return render(request, 'catalogbooks/first.html', context)


class BookList(ListView):
    '''Класс для отображения списка книг на странице'''

    model = Books
    context_object_name = 'books_list'
    template_name = 'catalogbooks/book_list.html'
    paginate_by = 7

    def get_context_data(self, **kwargs):
        context = super(BookList, self).get_context_data(**kwargs)
        context['title'] = 'Список книг'
        return context


class BookDetail(DetailView):
    '''Класс для отображения одной конкретной книги'''

    model = Books
    template_name = 'catalogbooks/book_detail.html'
    context_object_name = 'specific_book'

    def get_context_data(self, **kwargs):
        context = super(BookDetail, self).get_context_data(**kwargs)
        context['title'] = Books.objects.get(pk=self.kwargs['pk'])
        return context


class AuthorList(ListView):
    '''Список авторов'''
    
    model = Author
    context_object_name = 'author_list'
    template_name = 'catalogbooks/author_list.html'
    paginate_by = 7

    def get_context_data(self, **kwargs):
        context = super(AuthorList, self).get_context_data(**kwargs)
        context['title'] = 'Список авторов'
        return context


class AuthorDetail(DetailView):
    '''Класс для отображения одного конкретного автора'''

    model = Author
    template_name = 'catalogbooks/author_detail.html'
    context_object_name = 'specific_author'

    def get_context_data(self, **kwargs):
        context = super(AuthorDetail, self).get_context_data(**kwargs)
        context['title'] = Author.objects.get(pk=self.kwargs['pk'])
        return context


class UserBookList(LoginRequiredMixin, ListView):
    '''Книги, которые взял в аренду зарегистрированный'''

    model = BookInstance
    template_name = 'catalogbooks/user_books_list.html'
    context_object_name = 'usersbooks'
    paginate_by = 7

    def get_queryset(self):
        return BookInstance.objects.filter(debtor=self.request.user).filter(book_status__exact='А').order_by('date_back')

    def get_context_data(self, **kwargs):
        context = super(UserBookList, self).get_context_data(**kwargs)
        context['title'] = f"Книги {self.request.user}"
        return context


class AllBookRent(PermissionRequiredMixin, ListView):
    '''Список всех книг в аренде (доступна только персоналу)'''

    permission_required = (
        "catalogbooks.can_mark_returned",
    )
    model = BookInstance
    template_name = 'catalogbooks/all_users_books.html'
    context_object_name = 'allusersbooks'
    paginate_by = 7

    def get_queryset(self):
        return BookInstance.objects.filter(book_status__exact='А').order_by('date_back', 'debtor')

    def get_context_data(self, **kwargs):
        context = super(AllBookRent, self).get_context_data(**kwargs)
        context['title'] = 'Книги в аренде'
        return context


@login_required
@permission_required('catalogbooks.can_mark_returned', raise_exception=True)
def new_or_renew(request, pk):
    '''Установка даты возврата'''

    object_bookinstance = get_object_or_404(BookInstance, pk=pk)

    if request.method == 'POST':
        form = BookRenewForm(request.POST)
        if form.is_valid():
            object_bookinstance.date_back = form.cleaned_data['new_date_back']
            object_bookinstance.save()
            return HttpResponseRedirect(reverse('allrentbooks'))
    else:
        inst_renew_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = BookRenewForm(initial={'new_date_back': inst_renew_date})
    context = {
        'title': 'Установка даты возврата',
        'form': form,
        'object_bookinstance': object_bookinstance,
    }
    return render(request, 'catalogbooks/instance_new_date.html', context)


class CreateAuthor(PermissionRequiredMixin, CreateView):
    '''Создание автора по модели Author'''

    permission_required = (
        "catalogbooks.create_book_bystaff",
    )
    model = Author
    fields = ['name', 'surname', 'date_birth', 'date_death']
    template_name = 'catalogbooks/create_author.html'


class UpdateAuthor(PermissionRequiredMixin, UpdateView):
    '''Изменение автора по модели Author'''

    permission_required = (
        "catalogbooks.create_book_bystaff",
    )
    model = Author
    context_object_name = 'author'
    fields = ['name', 'surname', 'date_birth', 'date_death']
    template_name = 'catalogbooks/update_author.html'

    def get_context_data(self, **kwargs):
        context = super(UpdateAuthor, self).get_context_data(**kwargs)
        context['title'] = f"Изменить: {Author.objects.get(pk=self.kwargs['pk'])}"
        return context


class DeleteAuthor(PermissionRequiredMixin, DeleteView):
    '''Удаление автора по модели Author'''

    permission_required = (
        "catalogbooks.create_book_bystaff",
    )
    model = Author
    context_object_name = 'author'
    template_name = 'catalogbooks/delete_author.html'
    success_url = reverse_lazy('author')

    def get_context_data(self, **kwargs):
        context = super(DeleteAuthor, self).get_context_data(**kwargs)
        context['title'] = f"Удалить: {Author.objects.get(pk=self.kwargs['pk'])}"
        return context


class CreateBook(PermissionRequiredMixin, CreateView):
    '''Создаём книгу'''

    permission_required = (
        "catalogbooks.create_book_bystaff",
    )
    model = Books
    fields = ['title', 'author', 'language', 'genre', 'summary', 'isbn']
    template_name = 'catalogbooks/create_book.html'


class UpdateBook(PermissionRequiredMixin, UpdateView):
    '''Обновляем книгу'''

    permission_required = (
        "catalogbooks.create_book_bystaff",
    )
    model = Books
    context_object_name = 'book'
    fields = ['title', 'author', 'language', 'genre', 'summary', 'isbn']
    template_name = 'catalogbooks/update_book.html'

    def get_context_data(self, **kwargs):
        context = super(UpdateBook, self).get_context_data(**kwargs)
        context['title'] = f"Изменить: {Books.objects.get(pk=self.kwargs['pk']).title}"
        return context


class DeleteBook(PermissionRequiredMixin, DeleteView):
    '''Удаляем книгу'''

    permission_required = (
        "catalogbooks.create_book_bystaff",
    )
    model = Books
    context_object_name = 'book'
    template_name = 'catalogbooks/delete_book.html'
    success_url = reverse_lazy('books')

    def get_context_data(self, **kwargs):
        context = super(DeleteBook, self).get_context_data(**kwargs)
        context['title'] = f"Удалить: {Books.objects.get(pk=self.kwargs['pk']).title}"
        return context
