from django.db import models

# Create your models here.

class Department(models.Model):
    Name = models.CharField(max_length=200)
    Description = models.CharField(max_length=500)
    Created_by = models.ForeignKey('accounts.Account',on_delete=models.CASCADE,related_name='createdby')
    Created_at = models.DateTimeField(auto_now_add=True)
    Last_Updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.Name