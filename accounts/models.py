from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class Contact(models.Model):
    user_id = models.IntegerField()
    property_id = models.IntegerField()
    property_name = models.CharField(max_length=120)
    message = models.TextField()

    def __str__(self):
        return str(self.property_name)
