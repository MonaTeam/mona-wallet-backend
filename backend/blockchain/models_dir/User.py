from hashlib import sha256

from django import forms
from django.db import models


class User(models.Model):
    name = models.CharField(null=False, max_length=15)
    password = models.CharField(null=False, max_length=70)

    # class Meta:
    #     app_label = 'blockchain'

    @property
    def balance(self):
        return self.wallet

    @classmethod
    def create(cls, data):
        form = UserForm(data)
        # print(form.is_valid())
        if not form.is_valid():
            return False

        user = form.save(commit=False)

        # print(cls.exists(user.inn))
        if cls.exists(user.inn):
            return False

        user.wallet = 1000
        user.password = cls.make_password(user.password)
        user.save()
        return True

    @classmethod
    def exists(cls, inn: int):
        try:
            user = User.objects.get(inn=inn)
            print(user)
            return user
        except:
            return None

    @classmethod
    def make_password(cls, password: str):
        return sha256(password.encode('utf-8')).hexdigest()

    @classmethod
    def login(cls, inn: int, password: str):
        user = User.objects.filter(pk=inn).first()
        if not user:
            return None
        if user.password != cls.make_password(password):
            return None
        return user

    @classmethod
    def delete_all(cls):
        User.objects.all().delete()


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('inn', 'name', 'password')
