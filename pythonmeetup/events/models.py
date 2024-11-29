from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    DoesNotExist = None
    ROLE_CHOICES = [
        ('listener', 'Listener'),
        ('speaker', 'Speaker'),
        ('organizer', 'Organizer'),
    ]

    roles = models.JSONField(default=list)
    telegram_id = models.BigIntegerField(unique=True, null=True, blank=True)
    telegram_username = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name="customuser_groups",
        blank=True,
        help_text="The groups this user belongs to.",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name="customuser_permissions",
        blank=True,
        help_text="Specific permissions for this user.",
    )

    def has_role(self, role: str) -> bool:
        """Check if the user has the specified role."""
        return role in self.roles

    def is_speaker(self) -> bool:
        """Check if the user is a speaker."""
        return self.has_role('speaker')

    def is_listener(self) -> bool:
        """Check if the user is a listener."""
        return self.has_role('listener')

    def is_organizer(self) -> bool:
        """Check if the user is an organizer."""
        return self.has_role('organizer')


class SpeakerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,
                                related_name="speaker_profile")
    biography = models.TextField(blank=True, null=True)
    technical_stack = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Speaker Profile"


class OrganizerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,
                                related_name="organizer_profile")
    organization_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Organizer Profile"


class Talk(models.Model):
    DoesNotExist = None
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


class ListenerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,
                                related_name="listener_profile")
    name = models.CharField(max_length=255)
    event = models.ForeignKey(EventProgram, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}'s Listener Profile"


class Question(models.Model):
    text = models.TextField()  # Текст вопроса
    talk = models.ForeignKey(Talk, related_name="questions", on_delete=models.CASCADE)  # Привязка к докладу
    user = models.ForeignKey(CustomUser, related_name="questions", on_delete=models.CASCADE)  # Привязка к пользователю (если необходимо)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Question by {self.user} for {self.talk}"


class EventRegistration(models.Model):
    listener = models.ForeignKey(ListenerProfile, on_delete=models.CASCADE,
                                 related_name="event_registrations")
    event_program = models.ForeignKey(EventProgram, on_delete=models.CASCADE,
                                      related_name="registrations")
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('listener', 'event_program')

    def __str__(self):
        return f"{self.listener.user.username} registered for {self.event_program.title}"
