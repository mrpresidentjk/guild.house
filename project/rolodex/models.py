from django.db import models


class AbstractRolodex(models.Model):

    is_working = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Email(AbstractRolodex, models.Model):

    email = models.EmailField()

    def __str__(self):
        return self.email


class Phone(AbstractRolodex, models.Model):

    phone = models.CharField(max_length=16)

    def __str__(self):
        return self.phone
