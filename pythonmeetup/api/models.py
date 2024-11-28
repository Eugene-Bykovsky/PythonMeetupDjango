from django.db import models


class Speaker(models.Model):
    full_name = models.CharField(max_length=150)
    tg_id = models.CharField(max_length=50, unique=True)
    tech_stack = models.TextField()

    def __str__(self):
        return self.full_name


class User(models.Model):
    tg_username = models.CharField(max_length=50)
    tg_id = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.tg_username


class Question(models.Model):
    question_text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='questions'
    )
    speaker = models.ForeignKey(
        Speaker,
        on_delete=models.CASCADE,
        related_name='questions'
    )

    def __str__(self):
        return f"Вопрос от {self.author.tg_username} к {self.speaker.full_name}"
