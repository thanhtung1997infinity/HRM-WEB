import uuid

from api_base.models import TimeStampedModel
from api_user.models import Banks, User
from django.db import models


class UserBanks(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    account_number = models.CharField(max_length=100)
    bank = models.ForeignKey(Banks, on_delete=models.CASCADE)
    branch = models.CharField(max_length=100, null=True, blank=True)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="user_bank"
    )

    class Meta:
        db_table = "hr_user_banks"
