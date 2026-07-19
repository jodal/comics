from typing import Any, Self

from django.contrib.auth.models import User
from django.db import models
from django.http import HttpRequest

class Invitation(models.Model):
    email: str
    inviter: User | None
    @classmethod
    def create(cls, email: str, inviter: User | None = None, **kwargs: Any) -> Self: ...
    def send_invitation(self, request: HttpRequest, **kwargs: Any) -> None: ...
