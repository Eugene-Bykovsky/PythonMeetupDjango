from rest_framework import serializers
from events.models import (EventProgram, Talk, Question, CustomUser,
                           ListenerProfile, EventRegistration)


# Сериализатор для программы мероприятия
class EventProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventProgram
        fields = ['id', 'title', 'description', 'start_date', 'end_date']


# Сериализатор для доклада
class TalkSerializer(serializers.ModelSerializer):
    speaker = serializers.CharField(source='speaker.user.username')
    speaker_telegram_id = serializers.IntegerField(
        source='speaker.user.telegram_id',
        required=False)

    class Meta:
        model = Talk
        fields = ['id', 'title', 'start_time', 'end_time', 'speaker',
                  'speaker_telegram_id']


# Сериализатор для создания вопросов
class QuestionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['text', 'talk']


class QuestionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['text', 'talk', 'user', 'created_at']


# Сериализатор для ролей пользователей
class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'roles', 'telegram_id',
                  'telegram_username']


# Сериализатор для регистрации пользователя
class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['telegram_id', 'telegram_username', 'phone_number']

    def create(self, validated_data):
        user = CustomUser.objects.create(**validated_data)
        user.roles.append('listener')  # Присваиваем роль слушателя
        user.save()

        # Создаем профиль слушателя
        ListenerProfile.objects.create(user=user)

        return user


# Сериализатор для регистрации на мероприятие
class EventRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventRegistration
        fields = ['listener', 'event_program']

    def create(self, validated_data):
        # Извлекаем данные из сериализатора
        telegram_id = validated_data['listener'].telegram_id
        event_program = validated_data['event_program']

        # Находим или создаем пользователя по telegram_id
        user, created = CustomUser.objects.get_or_create(
            telegram_id=telegram_id,
            defaults={'username': validated_data['listener'].name}
        )

        # Проверяем, есть ли у пользователя роль 'listener', если нет -
        # добавляем
        if not user.has_role('listener'):
            user.roles.append('listener')
            user.save()

        # Создаем запись о регистрации на мероприятие
        registration = EventRegistration.objects.create(
            listener=user.listener_profile,
            event_program=event_program
        )

        return registration
