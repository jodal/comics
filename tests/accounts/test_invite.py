from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from django.core import mail
from django.core.mail.backends.base import BaseEmailBackend
from django.urls import reverse
from invitations.utils import get_invitation_model

if TYPE_CHECKING:
    from collections.abc import Sequence

    from django.contrib.auth.models import User
    from django.core.mail import EmailMessage
    from django.test.client import Client
    from pytest_django.fixtures import SettingsWrapper


class RefusingEmailBackend(BaseEmailBackend):
    """An e-mail backend that is having none of it."""

    def send_messages(self, email_messages: Sequence[EmailMessage]) -> int:
        msg = "the mail server is on fire"
        raise OSError(msg)


def test_inviting_sends_an_invitation(
    db: None,
    client: Client,
    user: User,
) -> None:
    client.force_login(user)

    response = client.post(reverse("invite"), {"email": "bob@example.com"})

    assert response.status_code == 200

    invitation = get_invitation_model().objects.get(email="bob@example.com")
    assert invitation.inviter == user
    assert len(mail.outbox) == 1
    assert mail.outbox[0].to == ["bob@example.com"]


def test_inviting_without_an_email_is_a_bad_request(
    db: None,
    client: Client,
    user: User,
) -> None:
    client.force_login(user)

    response = client.post(reverse("invite"), {})

    assert response.status_code == 400
    assert not get_invitation_model().objects.exists()


def test_failing_to_send_leaves_no_invitation_behind(
    db: None,
    client: Client,
    user: User,
    settings: SettingsWrapper,
) -> None:
    settings.EMAIL_BACKEND = f"{__name__}.RefusingEmailBackend"
    client.force_login(user)

    with pytest.raises(OSError, match="on fire"):
        client.post(reverse("invite"), {"email": "bob@example.com"})

    assert not get_invitation_model().objects.exists()
    assert len(mail.outbox) == 0
