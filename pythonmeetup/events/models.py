from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('listener', 'Listener'),
        ('speaker', 'Speaker'),
        ('organizer', 'Organizer'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES,
                            default='listener')
    telegram_id = models.BigIntegerField(unique=True, null=True, blank=True)
    telegram_username = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    groups = models.ManyToManyField(
        'auth.Group', related_name='customuser_groups', blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission', related_name='customuser_permissions', blank=True
    )


class SpeakerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,
                                related_name="speaker_profile")
    biography = models.TextField(blank=True, null=True)
    technical_stack = models.TextField(blank=True, null=True)


class ListenerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,
                                related_name="listener_profile")
    telegram_username = models.CharField(max_length=50, blank=True, null=True)
    telegram_id = models.BigIntegerField(unique=True, null=True, blank=True)


class OrganizerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,
                                related_name="organizer_profile")
    organization_name = models.CharField(max_length=100, blank=True, null=True)


class Question(models.Model):
    listener = models.ForeignKey(ListenerProfile, on_delete=models.CASCADE,
                                 related_name="questions")
    speaker = models.ForeignKey(SpeakerProfile, on_delete=models.CASCADE,
                                related_name="questions")
    question_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Talk(models.Model):
    speaker = models.ForeignKey(SpeakerProfile, on_delete=models.CASCADE,
                                related_name="talks")
    title = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    actual_start_time = models.DateTimeField(blank=True, null=True)
    actual_end_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} by {self.speaker.user.username}"


class EventProgram(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    talks = models.ManyToManyField(Talk, related_name="event_programs")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
