from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.http import HttpResponseRedirect

from userapp.models import User
from .forms import *


def administration(request):
    if not request.session.has_key('id'):
        return HttpResponseRedirect('/')

    id = request.session['id']
    if not User.objects.get(id=id).role == 'A':
        return HttpResponseRedirect('/')

    template = loader.get_template('administration-home.html')
    context = {

    }
    return HttpResponse(template.render(context, request))


def admins(request):
    if not request.session.has_key('id'):
        return HttpResponseRedirect('/')

    id = request.session['id']
    if not User.objects.get(id=id).role == 'A':
        return HttpResponseRedirect('/')

    template = loader.get_template('administration-admins.html')
    admin_list = User.objects.filter(role='A')
    context = {
        'admin_list' : admin_list,
        'admin_count' : len(admin_list),
        'addAdminForm' : AddAdminForm(),
    }
    return HttpResponse(template.render(context, request))
