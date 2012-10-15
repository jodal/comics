from tastypie.authorization import Authorization


class SubscriptionsAuthorization(Authorization):
    def is_authorized(self, request, object=None):
        return True

    def apply_limits(self, request, object_list):
        if request and hasattr(request, 'user'):
            return object_list.filter(userprofile__user=request.user)

        return object_list.none()
