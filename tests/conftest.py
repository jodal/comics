import pytest
from django.core.management import call_command
from django.test import override_settings


@pytest.fixture(scope="session", autouse=True)
def staticfiles(tmp_path_factory):
    with override_settings(
        STATIC_ROOT=tmp_path_factory.mktemp("static"),
        COMPRESS_ENABLED=False,
    ):
        call_command("collectstatic", "--noinput")
        yield
