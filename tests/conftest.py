import pytest
from django.core.management import call_command
from django.test import override_settings


@pytest.fixture(scope="session", autouse=True)
def staticfiles(tmp_path_factory):
    static_root = tmp_path_factory.mktemp("static")
    with override_settings(STATIC_ROOT=static_root):
        call_command("collectstatic", "--noinput")
        yield
