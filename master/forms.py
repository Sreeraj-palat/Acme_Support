from django import forms
from django.forms import ModelForm, widgets
from accounts.models import Account
from master.models import Department, Ticket



class create_user_form(forms.ModelForm):

    class Meta:
        model = Account
        fields = ['name', 'email','username', 'phone_number', 'department','role', 'password']
        

    def __init__(self, *args, **kwargs):
        super(create_user_form,self).__init__(*args,**kwargs)        
        for field in self.fields:
            self.fields[field].widget.attrs['class'] =  'form-control' 





class create_department_form(forms.ModelForm):

    class Meta:
        model = Department
        fields = ['Name', 'Description']
        

    def __init__(self, *args, **kwargs):
        super(create_department_form,self).__init__(*args,**kwargs)        
        for field in self.fields:
            self.fields[field].widget.attrs['class'] =  'form-control' 



class add_ticket_form(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = ['subject', 'description', 'priority']
        

    def __init__(self, *args, **kwargs):
        super(add_ticket_form,self).__init__(*args,**kwargs)        
        for field in self.fields:
            self.fields[field].widget.attrs['class'] =  'form-control'   




class CreateTicket(forms.Form):
    CHOICE = (
        ('high','high'),
        ('medium','medium'),
        ('low','low'),
    )
    subject = forms.CharField(max_length=200)
    description = forms.CharField(max_length=500,widget=forms.Textarea(attrs={"rows":5, "cols":20}))
    priority = forms.ChoiceField(choices=CHOICE)
    email = forms.CharField(max_length=100)
    phone_number = forms.CharField(max_length=100)
        
    def __init__(self, *args, **kwargs):
        super(CreateTicket, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"                      


