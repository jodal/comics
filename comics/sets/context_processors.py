from comics.sets.models import UserSet

def user_set(request):
    try:
        user_set = UserSet.objects.get(user=request.user)
        return {
            'user_set': user_set,
            'user_set_comics': user_set.comics.all(),
        }
    except UserSet.DoesNotExist:
        return {}
