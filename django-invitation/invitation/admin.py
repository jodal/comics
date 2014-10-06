from django.contrib import admin

from invitation.models import InvitationKey, InvitationUser


@admin.register(InvitationKey)
class InvitationKeyAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'from_user', 'date_invited', 'key_expired')


@admin.register(InvitationUser)
class InvitationUserAdmin(admin.ModelAdmin):
    list_display = ('inviter', 'invitations_remaining')
