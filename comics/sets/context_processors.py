def user_set(request):
    if hasattr(request, 'user_set'):
        return {
            'user_set': request.user_set,
            'user_set_comics': request.user_set.comics.all(),
        }
    else:
        return {}
