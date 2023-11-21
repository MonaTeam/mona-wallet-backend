from hashlib import sha256

from django import forms
from django.db import models


class User(models.Model):
    icon = models.ImageField(upload_to='user/icon/')
    email = models.EmailField()
    username = models.CharField(null=False, max_length=15)
    password = models.CharField(null=False, max_length=70)

    # class Meta:
    #     app_label = 'blockchain'

    def __str__(self):
        return f'User №{self.pk} name: {self.username}'

    @property
    def balance(self):
        return len(self.user_coins)

    @classmethod
    def create(cls, data):
        form = UserForm(data)
        if not form.is_valid():
            return False


        '''TODO: move checking to middleware'''

        user = form.save(commit=False)

        if cls.exists(user.inn):
            return False

        user.password = cls.make_password(user.password)
        user.save()
        return True

    @classmethod
    def exists(cls, inn: int):
        try:
            return User.objects.get(inn=inn)
        except:
            return None

    @classmethod
    def make_password(cls, password: str):
        return sha256(
            password.encode('utf-8')
        ).hexdigest()

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
        fields = ()
