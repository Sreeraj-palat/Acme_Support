from django.db import models

from accounts.models import Account

# Create your models here.

class Department(models.Model):
    Name = models.CharField(max_length=200)
    Description = models.CharField(max_length=500)
    Created_by = models.ForeignKey('accounts.Account',on_delete=models.CASCADE,related_name='createdby')
    Created_at = models.DateTimeField(auto_now_add=True)
    Last_Updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.Name


class Ticket(models.Model):
    High = 1
    Medium = 2
    Low = 3

    PRIORITY_CHOICES = (
          (High, 'High'),
          (Medium, 'Medium'),
          (Low, 'Low'),
      )
    user = models.ForeignKey(Account,on_delete=models.CASCADE,null=True, blank=True)
    ticket_id = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    priority = models.PositiveSmallIntegerField(choices=PRIORITY_CHOICES, blank=True, null=True)
    email = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.subject