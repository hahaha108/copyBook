from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.generic import ListView, DetailView

import utils
from books.models import Book, Chapter

class IndexView(ListView):
    model = Book
    template_name = 'index.html'
    context_object_name = 'booklist'
	
	paginate_by = 6

    def get_context_data(self, **kwargs):
        # 先调用父类的方法，获取默认的context
        context = super().get_context_data(**kwargs)
        paginator = context.get('paginator')
        page = context.get('page_obj')
        start, end = utils.custompaginator(paginator.num_pages, page.number, 10)
        context.update({
            'page_range': range(start, end + 1)
        })
        return context

class BookListView(IndexView):


    def get_queryset(self):

        return super(BookListView, self).get_queryset().filter(tag_id = self.kwargs.get('pk'))


# class AuthorView(DetailView):
#     model = Author
#     template_name = 'author/detail.html'
#     context_object_name = 'author'

# def author_view(request, pk):
#     author = Author.objects.get(id=pk)
#     return render(request,'author/detail.html',context={'author':author})

class BookView(DetailView):
    model = Book
    template_name = 'book/detail.html'
    context_object_name = 'book'

# def book_view(request,pk):
#     book = Book.objects.get(id = pk)
#     return render(request,'book/detail.html',context={'book':book})

class ChapterView(DetailView):
    model = Chapter
    template_name = 'book/chapter.html'
    context_object_name = 'chapter'


# def chapter_view(request,pk):
#     chapter = Chapter.objects.get(id = pk)
#     return render(request,'book/chapter.html',context={'chapter':chapter})
