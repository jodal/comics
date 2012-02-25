from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

@login_required
def new_secret_key(request):
    """Generate a new secret key for the current user"""

    if request.method == 'POST':
        user_profile = request.user.get_profile()
        user_profile.generate_new_secret_key()
        user_profile.save()
        messages.info(request, 'A new secret key was generated.')
        return HttpResponseRedirect(reverse('account_settings'))

    return render(request, 'accounts/new_secret_key.html')
