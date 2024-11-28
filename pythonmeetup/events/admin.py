from django.contrib import admin
from .models import (CustomUser, SpeakerProfile, ListenerProfile,
                     OrganizerProfile, Question, Talk, EventProgram)

admin.site.register(CustomUser)
admin.site.register(SpeakerProfile)
admin.site.register(ListenerProfile)
admin.site.register(OrganizerProfile)
admin.site.register(Question)
admin.site.register(Talk)
admin.site.register(EventProgram)