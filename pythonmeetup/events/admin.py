from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (CustomUser, SpeakerProfile, ListenerProfile,
                     OrganizerProfile, Question, Talk, EventProgram)


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = (
        'username', 'telegram_id', 'email', 'first_name', 'last_name',
        'is_active',
        'is_staff')
    search_fields = (
        'username', 'email',
        'telegram_id')
    ordering = ('username',)

    fieldsets = UserAdmin.fieldsets + (
        (None,
         {'fields': ('telegram_id', 'telegram_username', 'phone_number')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None,
         {'fields': ('telegram_id', 'telegram_username', 'phone_number')}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(SpeakerProfile)
admin.site.register(ListenerProfile)
admin.site.register(OrganizerProfile)
admin.site.register(Question)
admin.site.register(Talk)
admin.site.register(EventProgram)
