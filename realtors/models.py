from django.db import models
from datetime import datetime

from django.contrib.auth.hashers import make_password, check_password


# Create your models here.
class Realtor(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50, unique=True)
    website = models.CharField(max_length=60, unique=True)
    company_assoicated = models.CharField(max_length=100, unique=True)
    photo = models.ImageField(upload_to='uploads/%y/%m/%d')
    hire_date = models.DateTimeField(default=datetime.now, blank=True, db_index=True)

    def __str__(self):
        return self.name



