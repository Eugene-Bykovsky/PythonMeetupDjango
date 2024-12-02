from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (EventProgramViewSet, TalkViewSet, QuestionViewSet,
                    UserRoleViewSet, EventRegistrationViewSet, CheckRoleViewSet
                    )

router = DefaultRouter()
router.register(r'event-programs', EventProgramViewSet)
router.register(r'talks', TalkViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'users', UserRoleViewSet)
router.register(r'event-registrations', EventRegistrationViewSet)
router.register(r'', CheckRoleViewSet, basename='check-role')

urlpatterns = [
    path('', include(router.urls)),
]
