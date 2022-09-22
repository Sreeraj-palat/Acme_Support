from django import forms
from django.forms import ModelForm, widgets
from accounts.models import Account



class create_user_form(forms.ModelForm):

    class Meta:
        model = Account
        fields = ['name', 'email','username', 'phone_number', 'department','role', 'password']
        

    def __init__(self, *args, **kwargs):
        super(create_user_form,self).__init__(*args,**kwargs)        
        for field in self.fields:
            self.fields[field].widget.attrs['class'] =  'form-control' 