from django.db import models

class Speaker(models.Model):
	full_name = models.CharField(max_lenght=150)
	tg_id = model.CharField(max_lenght, unique=True)
	tech_stack = models.TextField()

	def __str__(self):
		return self.full_name