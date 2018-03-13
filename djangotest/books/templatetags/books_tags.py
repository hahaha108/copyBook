from django import template

from books.models import Book, Tag,Chapter

register = template.Library()

@register.simple_tag
def get_recent_books(num=5):
    return Book.objects.all()[:num]

@register.simple_tag
def get_tags(num=5):
    return Tag.objects.all()[:num]

@register.simple_tag
def get_chapter(bookID):
    return Chapter.objects.filter(book_id=bookID).order_by('number')