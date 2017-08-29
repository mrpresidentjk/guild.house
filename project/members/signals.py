# -*- coding: utf-8 -*-


def create_rolodex(sender, instance, **kwargs):
    if type(self.email) == str:
        self.email = Email.objects.get_or_create(email=self.email)

    if type(self.phone) == str:
        self.phone = Phone.objects.get_or_create(phone=self.phone)
