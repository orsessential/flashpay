import uuid
from decimal import Decimal

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from accounts.models import UserWallet

from model_utils import Choices

class Wallet(models.Model):
    """ Wallet model. Stores wallet related details.
    """

    user = models.OneToOneField(
        UserWallet, null=True, on_delete=models.SET_NULL,
        related_name='wallet'
    )

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    balance = models.DecimalField(
        _('Wallet Balance'), max_digits=10, decimal_places=2, default=0
    )
    STATUS = Choices(
        (1, "disable", "disable"),
        (2, "enable", "enable")
    )
    status = models.PositiveIntegerField(choices=STATUS, default=STATUS.enable)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [['user', 'uuid']]

    def __str__(self):
        return str(self.uuid)


