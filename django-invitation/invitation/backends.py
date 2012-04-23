from registration.backends.default import DefaultBackend
from invitation.models import InvitationKey

class InvitationBackend(DefaultBackend):

    def post_registration_redirect(self, request, user, *args, **kwargs):
        """
        Return the name of the URL to redirect to after successful
        user registration.

        """
        invitation_key = request.REQUEST.get('invitation_key')
        key = InvitationKey.objects.get_key(invitation_key)
        if key:
            key.mark_used(user)

        return ('registration_complete', (), {})
