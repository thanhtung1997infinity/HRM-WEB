import uuid

from api_base.models import TimeStampedModel
from api_user.models import User
from common.constants.user_constants import Relationships
from django.db import models


class UserFamilyMembers(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True)
    relationship = models.CharField(max_length=10, choices=Relationships.RELATIONSHIPS)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_family")

    class Meta:
        db_table = "hr_user_family_members"
