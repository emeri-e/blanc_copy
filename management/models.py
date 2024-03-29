from django.db import models

# Create your models here.

class BitgoWallet(models.Model):
    class Type(models.TextChoices):
        TRX = 'ttrx', 'TRON'
        SOL = 'tsol', 'Solana'
        POLYGON = 'tpolygon', 'Polygon'

    wallet_id = models.CharField(max_length=50, editable=False)
    _type = models.CharField(max_length=20, choices=Type.choices)
    
    @classmethod
    def from_dict(cls, data):
        return cls.objects.bulk_create(data)