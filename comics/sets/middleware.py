from comics.sets.models import UserSet


class SetMiddleware(object):
    def process_request(self, request):
        if request.user.is_active:
            request.user_set, _ = UserSet.objects.get_or_create(
                user=request.user)
        return None
