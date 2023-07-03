from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/')
    club_id = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.username}'

    def save(self, *args, **kwargs):
        #self.last_name = kwargs.get('last_name')
        #self.first_name = kwargs.get('first_name')
        super(CustomUser, self).save(*args, **kwargs)
