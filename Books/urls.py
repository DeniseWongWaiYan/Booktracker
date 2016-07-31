from django.conf.urls import url
from . import views

urlpatterns = [
   url(r'^search$', views.SearchBookView, name = 'searchbooks'),
   url(r'^detail/(?P<slug>[-\w]+)/(?P<ISBN>[-\d]+)/$', views.BookDetailView, name='detail'),
   url(r'^createchallenge/', views.ChallengeCreateView, name='createchallenge'),
   url(r'^like/', views.book_like, name='like'),
   url(r'^$', views.BookListView, name='book_list',),
   url(r'^additem/', views.add_book, name='add_book'),
   ]
