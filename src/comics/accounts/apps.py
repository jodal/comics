from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = "comics.accounts"

    def ready(self) -> None:
        # Imported here, and not at module level, because Django requires
        # the app registry to be populated before the models the receivers
        # build on can be imported.
        from comics.accounts import signals  # noqa: PLC0415

        signals.connect()
