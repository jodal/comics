from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.contrib.auth.models import User
    from django.http import HttpRequest

    from comics.accounts.models import UserProfile

    class ComicsUser(User):
        """A user, as seen by type checkers.

        Adds the reverse accessors that the type checker cannot derive from
        the related models.
        """

        comics_profile: UserProfile

    class AuthenticatedHttpRequest(HttpRequest):
        """A request guaranteed to have a logged-in user.

        For annotating views wrapped in @login_required.
        """

        # Deliberately narrows the mutable `user` attribute, which trips
        # the invariance rule.
        user: ComicsUser  # pyright: ignore[reportIncompatibleVariableOverride]
