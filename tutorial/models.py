from django.db import models
from .apps import APP_NAME
from django.utils.translation import gettext as _
# Create your models here.
from app.models import Page
class Lesson(Page):
       

    class Meta:
        verbose_name = _("Lesson")
        verbose_name_plural = _("Lessons")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("Lesson_detail", kwargs={"pk": self.pk})
