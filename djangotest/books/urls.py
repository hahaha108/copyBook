from django.conf.urls import url

from books.views import IndexView,  BookView,ChapterView,BookListView

urlpatterns = [
    url(r'index/$',IndexView.as_view(), name='index'),
    url(r'^booklist/(?P<pk>\d+)/$', BookListView.as_view(), name='booklist'),
    url(r'^book/(?P<pk>\d+)/$',BookView.as_view(),name='book'),
    url(r'^chapter/(?P<pk>\d+)/$',ChapterView.as_view(),name='chapter'),
]
