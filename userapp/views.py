from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.http import HttpResponseRedirect

from .models import *
from .forms import *

import json

# Create your views here.

def index(request):

    if request.session.has_key('id'):
        return HttpResponseRedirect('/home')

    template = loader.get_template('index.html')
    context = {
        'loginForm' : LoginForm(),
        'registerForm' : RegisterForm(),
    }
    return HttpResponse(template.render(context, request))


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if not form.is_valid():
            return HttpResponseRedirect('/')

        _first_name = form.cleaned_data['first_name']
        _last_name = form.cleaned_data['last_name']
        _email = form.cleaned_data['email']
        _student_id = form.cleaned_data['student_id']
        _password = form.cleaned_data['password']
        _confirm_password = form.cleaned_data['confirm_password']

        if(_password != _confirm_password):
            HttpResponseRedirect('/')

        user = User(first_name=_first_name, last_name=_last_name, email=_email, student_id=_student_id, password=_password)

        try:
            user.save()
        except:
            print('Error creating user with student id ' + str(_student_id))
            return HttpResponseRedirect('/')

        request.session['id'] = user.id
        request.session.modified = True
        return HttpResponseRedirect('/home/' + str(user.id))



def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if not form.is_valid():
            return HttpResponseRedirect('/')
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']

        x = User.objects.filter(email=email, password=password).first()

        if(x == None):
            return HttpResponseRedirect('/')

        request.session['id'] = x.id
        request.session.modified = True
        return HttpResponseRedirect('/home')


def logout(request):
    if request.session.has_key('id'):
        del request.session['id']
        request.session.modified = True
    return HttpResponseRedirect('/')


def home(request):
    if not request.session.has_key('id'):
        return HttpResponseRedirect('/')

    id = request.session['id']

    template = loader.get_template('user-account.html')
    context = {
        'user' : User.objects.get(id=id),
    }
    return HttpResponse(template.render(context, request))


def add_book(request):
    if not request.session.has_key('id'):
        return HttpResponseRedirect('/')
    # if request.method == 'GET':
    #     print('geting form')
    #     form = AddBookForm(request.GET)
    #     return render(request, 'add-book.html', form)
    template = loader.get_template('add-book.html')
    context = {
        'addBookForm' : AddBookForm(),
    }
    return HttpResponse(template.render(context, request))


def get_book_suggestion(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        books = Book.objects.filter(name__icontains = q)
        # authors_ = Author.objects.filter(name__contains = q)[:5]
        # for author in authors_:
        books = (books | Book.objects.filter(authors__name__icontains=q)).distinct()
        # books = Book.objects.all()
        results = []
        for book in books:
            book_json = {}
            value = book.name + ' by '
            for author in book.authors.all():
                value = value + author.name + ', '
            value = value[:-2]
            book_json['value'] = value
            book_json['id'] = book.id
            results.append(book_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def add_product(request):
    if not request.session.has_key('id'):
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        form = AddBookForm(request.POST)
        if not form.is_valid():
            # template = loader.get_template('add-book.html')
            print('form error')
            return render(request, 'add-book.html', {'addBookForm': form})

        product = Product()
        product.owner = User.objects.get(id=request.session['id'])

        bookid = form.cleaned_data['bookid']
        product.book = Book.objects.get(id=bookid)

        product.print_status = form.cleaned_data['print_status']
        product.condition = form.cleaned_data['condition']

        try:
            product.edition = int(form.cleaned_data['edition'])
        except:
            pass

        try:
            product.price = int(form.cleaned_data['price'])
        except:
            product.price = 0
        try:
            product.save()
        except Exception as e:
            print('Error saving product from user ' + product.owner.student_id + ' on ' + product.book.name)
            form.success = 2
            return render(request, 'add-book.html', {'addBookForm': form})
        form = AddBookForm()
        form.success = 1
        return render(request, 'add-book.html', {'addBookForm': form})


def add_new_book(request):
    if not request.session.has_key('id'):
        return HttpResponseRedirect('/')
    if request.is_ajax():
        name = request.POST['name']
        authors_name = request.POST['authors'].split(',')

        book = Book.objects.filter(name=name).first()
        if book == None:
            book = Book(name=name)
            book.save()
        else:
            bookid = book.id
            mimetype = 'application/json'
            return HttpResponse(bookid, mimetype)

        for author_name in authors_name:
            author = Author.objects.filter(name=author_name).first()
            if author == None:
                author = Author(name=author_name)
                author.save()
            book.authors.add(author)
        bookid = book.id
    else:
        bookid = 0
    mimetype = 'application/json'
    return HttpResponse(bookid, mimetype)


def user_books(request):
    if not request.session.has_key('id'):
        return HttpResponseRedirect('/')
    id = request.session['id']
    template = loader.get_template('user-books.html')
    none = '-'
    context = {
        'userProducts' : Product.objects.filter(owner__id=id),
        'none' : none,
    }
    return HttpResponse(template.render(context, request))


def notifications(request):
    if not request.session.has_key('id'):
        return HttpResponseRedirect('/')
    template = loader.get_template('notifications.html')
    context = {

    }
    return HttpResponse(template.render(context, request))


def search_books(request):
    if not request.session.has_key('id'):
        return HttpResponseRedirect('/')
    template = loader.get_template('search-books.html')
    context = {

    }
    return HttpResponse(template.render(context, request))


def user_requests(request):
    if not request.session.has_key('id'):
        return HttpResponseRedirect('/')
    template = loader.get_template('user-requests.html')
    context = {

    }
    return HttpResponse(template.render(context, request))