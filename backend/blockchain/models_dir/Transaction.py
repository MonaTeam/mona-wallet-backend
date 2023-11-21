from hashlib import sha256

from django.db import models

from backend.blockchain.models_dir.Block import Block
from backend.blockchain.models_dir.Coin import Coin
from backend.blockchain.models_dir.User import User


class Transaction(models.Model):
    block = models.ForeignKey(Block, on_delete=models.PROTECT, related_name='block_transactions')
    sender = models.ForeignKey(User, related_name='sent_transactions', on_delete=models.PROTECT)
    recipient = models.ForeignKey(User, related_name='received_transactions', on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    forwarded_coins = models.ManyToManyField(Coin, related_name='transactions')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Transaction №{self.pk}. {self.sender} send {self.amount} coins to {self.recipient} '

    @property
    def hash(self):
        return sha256(
            u'{}{}{}{}'.format(
                self.pk,
                self.sender,
                self.recipient,
                self.amount,
                self.timestamp).encode('utf-8')).hexdigest()

    @classmethod
    def create(cls, sender, recipient, amount):

        if Block.is_last_filled(): Block.create()
        last_block = Block.last()

        Transaction.objects.create(
            block=last_block,
            sender=sender,
            recipient=recipient,
            amount=amount
        )

        '''TODO: Adding coins to user'''

        last_block.hash__(save=True)

    @classmethod
    def delete_all(cls):
        Transaction.objects.all().delete()
