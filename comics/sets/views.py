from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.decorators.cache import never_cache

from comics.core.models import Comic
from comics.sets.models import Set


@login_required
@never_cache
def user_set_toggle_comic(request):
    """Add to or remove from comic to the current user's set"""

    if request.method != 'POST':
        response = HttpResponse(status=405)
        response['Allowed'] = 'POST'
        return response

    comic = get_object_or_404(Comic, slug=request.POST['comic'])

    if 'add_comic' in request.POST:
        request.user_set.comics.add(comic)
        if not request.is_ajax():
            messages.info(request, 'Added "%s" to my comics' % comic.name)
    elif 'remove_comic' in request.POST:
        request.user_set.comics.remove(comic)
        if not request.is_ajax():
            messages.info(request, 'Removed "%s" from my comics' % comic.name)

    if request.is_ajax():
        return HttpResponse(status=204)
    else:
        return HttpResponseRedirect(reverse('userset-latest'))


@login_required
@never_cache
def user_set_import_named_set(request):
    """Import comics from a named set into the current user's set"""

    if request.method == 'POST':
        try:
            named_set = Set.objects.get(name=request.POST['namedset'])
        except Set.DoesNotExist:
            messages.error(request, 'No comic set named "%s" found.' %
                request.POST['namedset'])
            return HttpResponseRedirect(reverse('import_named_set'))

        count_before = len(request.user_set.comics.all())
        request.user_set.comics.add(*named_set.comics.all())
        count_added = len(request.user_set.comics.all()) - count_before
        messages.info(request,
            '%d comic(s) was added to your comics selection.' % count_added)
        if count_added > 0:
            return HttpResponseRedirect(reverse('userset-latest'))
        else:
            return HttpResponseRedirect(reverse('import_named_set'))

    return render(request, 'sets/import_named_set.html', {
        'active': {
            'account': True,
            'import_named_set': True,
        }
    })
