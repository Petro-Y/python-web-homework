from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from .models import *

def root(request):
    res=''
    for book in Book.objects.all():
        item=[book.title]
        for ba in BookAuthor.objects.filter(book_id=book.id):
            for author in Author.objects.filter(id=ba.author_id):
                item+=[author.name]
        res+='<li>%s - %s</li>'%(', '.join(item[1:]), item[0])
    res='Перелік книг:<ul>%s</ul>'%res
    return HttpResponse(res)
