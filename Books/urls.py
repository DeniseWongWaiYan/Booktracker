from django.conf.urls import url
from . import views

urlpatterns = [
   url(r'^find/', views.findbookview, name = 'searchbooks'),
   url(r'^detail/(?P<slug>[-\w]+)/(?P<ISBN>[-\d]+)/', views.BookDetailView, name='detail'),
   url(r'^createchallenge/', views.ChallengeCreateView, name='createchallenge'),
   url(r'^like/', views.book_like, name='like'),
   url(r'^list', views.dummy, name='book_list',),
   url(r'^all/', views.BookListView, name='all'),
   ]
