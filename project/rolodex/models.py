from django.db import models


class Email(models.Model):

    email = models.EmailField()


class Phone(models.Model):

    phone = models.CharField(max_length=16)
