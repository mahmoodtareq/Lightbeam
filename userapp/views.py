from django.db import IntegrityError
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.db.models import Max, Min

from .models import *
from .forms import *
from .search import *

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
    user = User.objects.get(id=id)

    form = ProfileForm(initial={'address': user.address, 'mobile_no': user.mobile_no})

    template = loader.get_template('user-account.html')
    context = {
        'user': user,
        'profileForm': form,
    }
    return HttpResponse(template.render(context, request))


def save_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if not form.is_valid():
            return HttpResponseRedirect('/')

        _address = form.cleaned_data['address']
        _mobile_no = form.cleaned_data['mobile_no']

        user = User.objects.get(id=request.session['id'])

        user.address = _address
        user.mobile_no = _mobile_no

        user.save()

        template = loader.get_template('user-account.html')
        context = {
            'user': user,
            'profileForm': form,
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
        book.approval_status = 'P'
        book.save()
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
        'searchForm': SearchForm(),
        'result': [],
    }
    return HttpResponse(template.render(context, request))


def view_book(request, product_id):
    if not request.session.has_key('id'):
        return HttpResponseRedirect('/')
    template = loader.get_template('view-book.html')
    # product = Product.objects.filter(id=product_id)
    # print(product)

    context = {
        'product' : Product.objects.get(id=product_id),
    }
    return HttpResponse(template.render(context, request))


def profile(request, user_id):
    if not request.session.has_key('id'):
        return HttpResponseRedirect('/')
    template = loader.get_template('profile.html')
    # product = Product.objects.filter(id=product_id)
    # print(product)

    context = {
        'user' : User.objects.get(id=user_id),
    }
    return HttpResponse(template.render(context, request))


def search(request):
    if not request.session.has_key('id'):
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if not form.is_valid():
            return render(request, 'search-books.html', {'searchForm':form, 'result':[]})
        key = form.cleaned_data['query']
        choice = form.cleaned_data['search_for']
        id = request.session['id']
        result = []
        if choice == '':
            result = searchAll(key, id)
        else:
            if choice == 'B':
                result = searchBook(key, id)
            elif choice == 'A':
                result = searchAuthor(key, id)
            elif choice == 'C':
                result = searchCategory(key, id)

        serials = []
        for product in result:
            cnt = Serial.objects.filter(product=product).count()
            serials.append(cnt)
        return render(request, 'search-books.html', {'searchForm': form, 'result': result})


def user_requests(request):
    if not request.session.has_key('id'):
        return HttpResponseRedirect('/')
    id = request.session['id']
    template = loader.get_template('user-requests.html')
    serial = Serial.objects.filter(user__id=id)
    # print(serial.serial_no)

    context = {
    # from here
        'userRequests': Serial.objects.filter(user__id=id),

    # to here
    }
    return HttpResponse(template.render(context, request))


def book_request(request):
    if request.is_ajax():
        product_id = request.POST.get('product_id', '')
        type = request.POST.get('type', '')
        id = request.session['id']

        qsMax = Serial.objects.filter(product__id=product_id).aggregate(Max("serial_no"))

        qsMin = Serial.objects.filter(product__id=product_id).aggregate(Min("serial_no"))
        data = 0

        print(type)

        if type == 'book-the-book':
            if qsMax is None:
                data = 0
            else:
                serial = Serial()
                serial.product = Product.objects.get(id=product_id)
                serial.user = User.objects.get(id=id)
                serial.serial_no = 1
                serial.save()

                holder = CurrentHolder()
                holder.product = Product.objects.get(id=product_id)
                holder.holder = User.objects.get(id=id)
                holder.save()
                data = 1
        elif type == 'stand-in-queue':
            serial = Serial()
            serial.product = Product.objects.get(id=product_id)
            serial.user = User.objects.get(id=id)
            max_serial_no = qsMax['serial_no__max']
            min_serial_no = qsMin['serial_no__min']
            serial.serial_no = max_serial_no + 1
            serial.save()
            data = max_serial_no - min_serial_no + 2

        mimetype = 'application/json'
        return HttpResponse(data, mimetype)