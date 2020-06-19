from django.db import models

from djbver.db.models import GenericModel


class Payment(GenericModel):
    merchant_uid = models.CharField('상점코드', max_length=255)
    transaction_uid = models.CharField('결제코드', max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'payments'
        unique_together = ['transaction_uid', 'merchant_uid']
        verbose_name = '결제'
        verbose_name_plural = '결제들'