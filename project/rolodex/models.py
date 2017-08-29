from django.db import models


class Email(models.Model):

    email = models.EmailField()

    def __str__(self):
        return self.email


class Phone(models.Model):

    phone = models.CharField(max_length=16)

    def __str__(self):
        return self.phone
