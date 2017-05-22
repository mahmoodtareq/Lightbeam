from django import forms
from userapp.models import User

class AddAdminForm(forms.Form):
    name = forms.CharField(label='Name', max_length=50)
    id = forms.IntegerField(widget=forms.HiddenInput(), min_value=1, label='')
    def __init__(self, *args, **kwargs):
        super(AddAdminForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'