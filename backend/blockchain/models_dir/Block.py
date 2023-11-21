import os
from hashlib import sha256

from django.db import models
from dotenv import load_dotenv

load_dotenv()


class Block(models.Model):
    hash = models.CharField(max_length=70)
    previous_hash = models.CharField(max_length=70)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Block №{self.pk} hash: {self.hash}'

    def hash__(self, save=False):
        fields = []

        for field in self._meta.fields:
            print(field.name == 'pk')
            if field.name != 'pk' and field.name != 'hash':
                fields.append(field.value_to_string(self))

        fields.append(
            [trns.hash for trns in self.block_transactions.all()]
        )

        block_hash = sha256(
            (str(self.pk) + ''.join(fields)).encode()
        ).hexdigest()

        if save:
            self.hash = block_hash
            self.save()

        return block_hash

    @classmethod
    def create(cls):
        # print(cls.is_chain_valid())
        if not cls.is_chain_valid():
            return

        if not cls.is_last_filled():
            return

        hash_last = cls.last().hash__()
        Block(previous_hash=hash_last).save()
        return

    @classmethod
    def is_last_filled(cls) -> bool:
        if len(cls.last().transaction_set.all()) >= int(os.getenv('BLOCK_TRANSACTION_COUNT')):
            return True
        return False

    @classmethod
    def is_chain_valid(cls) -> bool:
        blocks = Block.objects.all().order_by('-pk')
        # print([str(blk) for blk in blocks])
        pointer = 0

        while pointer != len(blocks)-1:
            if blocks[pointer].previous_hash != blocks[pointer+1].hash__():
                return False

            pointer += 1
        return True

    @classmethod
    def last(cls):
        last_block = Block.objects.all().order_by('pk').last()

        if not last_block:
            cls.create_genesis_block()
            return cls.last()

        return last_block

    @classmethod
    def create_genesis_block(cls):
        Block(
            previous_hash='GENESIS'
        ).save()

    @classmethod
    def delete_all(cls):
        Block.objects.all().delete()
