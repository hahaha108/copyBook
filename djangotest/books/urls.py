from django.urls import path, re_path

from books.views import IndexView, BookView,ChapterView,BookListView

urlpatterns = [
    
    re_path(r'index/$',IndexView.as_view(), name='index'),
    re_path(r'^booklist/(?P<pk>\d+)/$', BookListView.as_view(), name='booklist'),
    re_path(r'^book/(?P<pk>\d+)/$',BookView.as_view(), name='book'),
    re_path(r'^chapter/(?P<pk>\d+)/$',ChapterView.as_view(), name='chapter'),
]
