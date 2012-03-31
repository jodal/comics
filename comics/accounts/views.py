from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

@login_required
def account_details(request):
    return render(request, 'accounts/details.html', {
        'active': {
            'account': True,
            'account_details': True,
        }
    })

@login_required
def secret_key(request):
    """Show and generate a new secret key for the current user"""

    if request.method == 'POST':
        user_profile = request.user.get_profile()
        user_profile.generate_new_secret_key()
        user_profile.save()
        messages.info(request, 'A new secret key was generated.')
        return HttpResponseRedirect(reverse('secret_key'))

    return render(request, 'accounts/secret_key.html', {
        'active': {
            'account': True,
            'secret_key': True,
        }
    })
