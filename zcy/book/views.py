# -*- coding: utf-8 -*-
#from django.template.loader import get_template
#from django.template import Context
#from django.shortcuts import render
from django.shortcuts import render_to_response
import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
import MySQLdb
from book.models import Author, Book
from django import forms
class BookForm(forms.ModelForm):
    ISBN = forms.IntegerField(widget=forms.NumberInput(attrs={"placeholder":"编号"}))
    Title = forms.CharField(max_length = 20,widget=forms.TextInput(attrs={"placeholder":"书名"}))
    Publisher = forms.CharField(max_length = 30,widget=forms.TextInput(attrs={"placeholder":"出版社"}))
    PublishDate = forms.CharField(max_length = 20,widget=forms.TextInput(attrs={"placeholder":"出版日期"}))
    Price = forms.CharField(max_length = 10,widget=forms.TextInput(attrs={"placeholder":"价格"}))
    class Meta:
        model = Book
        fields = "__all__"
        
class AuthorForm(forms.ModelForm):
    AuthorID = forms.IntegerField(widget=forms.NumberInput(attrs={"placeholder":"作者编号"}))
    Name = forms.CharField(max_length = 20,widget=forms.TextInput(attrs={"placeholder":"姓名"}))
    Age = forms.CharField(max_length = 10,widget=forms.TextInput(attrs={"placeholder":"年龄"}))
    Country = forms.CharField(max_length = 20,widget=forms.TextInput(attrs={"placeholder":"国家"}))
    class Meta:
        model = Author
        fields = "__all__"
class updateBookForm(forms.Form):
    ISBN = forms.IntegerField(widget=forms.TextInput(attrs={"readonly":True}))
    Title = forms.CharField(max_length=20)
    AuthorID = forms.ModelChoiceField(queryset=Author.objects.all(), empty_label=None)
    Publisher = forms.CharField(max_length=30)
    PublishDate = forms.CharField(max_length=20)
    Price = forms.CharField(max_length=10)

# Create your views here.

def index(request):
    if request.method == "POST":
        if "q" in request.POST:
            Name = request.POST.get('q')
            if Author.objects.filter(Name = Name):
                author = Author.objects.get(Name = Name)
                return HttpResponseRedirect("../searchbookbyauthor/"+str(author.AuthorID))
            else:
                return HttpResponseRedirect("/index/")
    booklist = Book.objects.all()
    authorlist = Author.objects.all()
    return render_to_response('index.html', locals())
def addbook(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/index/")
    else:
        form = BookForm()
    return render_to_response('addbook.html', {'form':form})
def addauthor(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/addbook/")
    else:
        form = AuthorForm()
    return render_to_response('addauthor.html', {'form':form})
def searchbookbyauthor(request,id):
    if request.method == "GET":
        author = Author.objects.get(AuthorID = id)
        booklist = author.book_set.all()
    return render_to_response('searchbookbyauthor.html', locals())
def searchallbybook(request, id):
    if request.method == "GET":
        book = Book.objects.get(Title = id)
        author = Author.objects.get(AuthorID = book.AuthorID.AuthorID)
    return render_to_response('searchallbybook.html', locals())
def deletebook(request, id):
    if request.method == "GET":
        if Book.objects.filter(Title = id):
            book = Book.objects.filter(Title = id).get(Title = id)
            book.delete()
    return HttpResponseRedirect("/index/")
#update book information
def updatebook(request, ISBN):
    book = Book.objects.get(ISBN = ISBN)
    data = {"ISBN":book.ISBN,
            "Title":book.Title,
            "AuthorID":book.AuthorID,
            "Publisher":book.Publisher,
            "PublishDate":book.PublishDate,
            "Price":book.Price}
    if request.method == "POST":
        form = updateBookForm(request.POST,initial=data)
        if form.is_valid():
            if form.has_changed():
                book.ISBN = form.cleaned_data['ISBN']
                book.Title = form.cleaned_data['Title']
                book.AuthorID = form.cleaned_data['AuthorID']
                book.Publisher = form.cleaned_data['Publisher']
                book.PublishDate = form.cleaned_data['PublishDate']
                book.Price = form.cleaned_data['Price']
                book.save()
            return HttpResponseRedirect("/searchallbybook/" + book.Title)
    else:
        form = updateBookForm(initial=data)
    return render_to_response('updatebook.html', {'form':form})
