from django.db import models

from backend.blockchain.models_dir.Transaction import Transaction
from backend.blockchain.models_dir.User import User


class Coin(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='user_coins')

    def __str__(self):
        return f'Coin №{self.pk} user: {self.user}'

