from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from events.models import (EventProgram, Talk, Question, CustomUser,
                           EventRegistration, ListenerProfile)
from .serializers import (EventProgramSerializer, TalkSerializer,
                          QuestionCreateSerializer, QuestionListSerializer,
                          UserRoleSerializer, UserRegistrationSerializer,
                          EventRegistrationSerializer)
from rest_framework.permissions import IsAuthenticated


# ViewSet для программы мероприятия
class EventProgramViewSet(viewsets.ModelViewSet):
    queryset = EventProgram.objects.all()
    serializer_class = EventProgramSerializer


# ViewSet для докладов
class TalkViewSet(viewsets.ModelViewSet):
    queryset = Talk.objects.all()
    serializer_class = TalkSerializer


# ViewSet для вопросов
class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return QuestionCreateSerializer
        return QuestionListSerializer

    def perform_create(self, serializer):
        talk_id = self.request.data.get('talk')
        user = self.request.user

        # Получаем доклад, к которому привязываем вопрос
        try:
            talk = Talk.objects.get(id=talk_id)
        except Talk.DoesNotExist:
            raise Response({"detail": "Talk not found"},
                           status=status.HTTP_404_NOT_FOUND)

        # Создаем вопрос с привязкой к докладу и пользователю
        serializer.save(user=user, talk=talk)


# ViewSet для пользователей
class UserRoleViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserRoleSerializer


# ViewSet для регистрации пользователей
class UserRegistrationViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer


# ViewSet для регистрации на мероприятия
class EventRegistrationViewSet(viewsets.ModelViewSet):
    queryset = EventRegistration.objects.all()
    serializer_class = EventRegistrationSerializer

    def create(self, request, *args, **kwargs):
        # Извлекаем данные из запроса
        event_id = request.data.get('event_id')
        telegram_id = request.data.get('telegram_id')
        name = request.data.get('name')

        if not event_id or not telegram_id or not name:
            return Response(
                {"detail": "Missing event_id, telegram_id or name"},
                status=status.HTTP_400_BAD_REQUEST)

        # Находим мероприятие
        try:
            event_program = EventProgram.objects.get(id=event_id)
        except EventProgram.DoesNotExist:
            return Response({"detail": "Event not found"},
                            status=status.HTTP_404_NOT_FOUND)

        # Создаем или находим пользователя
        user, created = CustomUser.objects.get_or_create(
            telegram_id=telegram_id,
            defaults={'username': name}
        )

        # Создаем профиль слушателя и обязательно привязываем его к событию
        listener_profile, created = ListenerProfile.objects.get_or_create(
            user=user,
            defaults={'name': name, 'event': event_program}
        )

        # Присваиваем роль 'listener', если она еще не добавлена
        if 'listener' not in user.roles:
            user.roles.append('listener')
            user.save()

        # Создаем запись в таблице регистрации
        registration = EventRegistration.objects.create(
            listener=listener_profile,
            event_program=event_program
        )

        # Сериализация данных для ответа
        serializer = EventRegistrationSerializer(registration)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CheckRoleViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['get'], url_path='check-role')
    def check_role(self, request):
        telegram_id = request.query_params.get('telegram_id')

        if not telegram_id:
            return Response(
                {"detail": "telegram_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = CustomUser.objects.get(telegram_id=telegram_id)
        except CustomUser.DoesNotExist:
            return Response(
                {"detail": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Получаем роли пользователя
        roles = user.roles

        return Response({"roles": roles}, status=status.HTTP_200_OK)
