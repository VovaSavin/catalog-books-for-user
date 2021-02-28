from django.urls import path
from .import views


urlpatterns = [
    path('', views.main_foo, name='first'),
    path('books/', views.BookList.as_view(), name='books'),
    path('books/<int:pk>', views.BookDetail.as_view(), name='books-detail'),
    path('author/', views.AuthorList.as_view(), name='author'),
    path('author/<int:pk>', views.AuthorDetail.as_view(), name='author_info'),
    path('mybooks/', views.UserBookList.as_view(), name='mybooks'),
    path('allrentbooks/', views.AllBookRent.as_view(), name='allrentbooks'),
    path('book/<uuid:pk>/renewdate', views.new_or_renew, name='renewdate'),
    path('author/create', views.CreateAuthor.as_view(), name='create-author'),
    path('author/<int:pk>/update',
         views.UpdateAuthor.as_view(), name='update-author'),
    path('author/<int:pk>/delete',
         views.DeleteAuthor.as_view(), name='delete-author'),
    path('book/create', views.CreateBook.as_view(), name='create-book'),
    path('book/<int:pk>/update', views.UpdateBook.as_view(), name='update-book'),
    path('book/<int:pk>/delete', views.DeleteBook.as_view(), name='delete-book'),
]
