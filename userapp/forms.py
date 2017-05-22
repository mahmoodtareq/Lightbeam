from django import forms
from django.utils.safestring import mark_safe
from .models import *

class HorizontalRadioRenderer(forms.RadioSelect.renderer):
  def render(self):
    return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))

class RegisterForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=30, min_length=2)
    last_name = forms.CharField(label='Last Name', max_length=30, min_length=2)
    email = forms.CharField(label='Email', max_length=50, min_length=5)
    student_id = forms.CharField(label='Student ID', max_length=7, min_length=7)
    password = forms.CharField(label='Password', max_length=30, min_length=8, widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm Password', max_length=30, min_length=8, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class LoginForm(forms.Form):
    email = forms.CharField(label='Email', max_length=50, min_length=5)
    password = forms.CharField(label='Password', max_length=30, min_length=8, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class AddBookForm(forms.Form):
    EDITIONS = [(0, 'Choose one')] + [(x, x) for x in range(1, 16)]
    bookname = forms.CharField(label='Book Name', max_length=50)
    # bookid = forms.IntegerField(label='Book ID', disabled=True, required=False)
    print_status = forms.ChoiceField(choices=Product.PRINT_STATUSES, widget=forms.RadioSelect(renderer=HorizontalRadioRenderer), required=False)
    condition = forms.ChoiceField(choices=Product.CONDITIONS, widget=forms.RadioSelect(renderer=HorizontalRadioRenderer), required=False)
    edition = forms.ChoiceField(choices=EDITIONS, required=False)
    price = forms.IntegerField(required=False)
    bookid = forms.IntegerField(widget=forms.HiddenInput(), min_value=1, label='')

    success = 0     # 0 = new, 1 = success, 2 = db error

    def __init__(self, *args, **kwargs):
        super(AddBookForm, self).__init__(*args, **kwargs)
        self.fields['bookname'].widget.attrs['class'] = 'form-control'
        self.fields['edition'].widget.attrs['class'] = 'form-control'
        self.fields['price'].widget.attrs['class'] = 'form-control'
