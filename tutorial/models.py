from django.db import models
from django.utils.translation import gettext as _
from django.shortcuts import reverse
from app.models import Page
from app.settings import ADMIN_URL
from .apps import APP_NAME



class Lesson(Page):

    def save(self):
        self.child_class='lesson'
        super(Lesson,self).save()

    class Meta:
        verbose_name = _("Lesson")
        verbose_name_plural = _("Lessons")

    def __str__(self):
        return self.title
    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/lesson/{self.pk}/change/'
    def get_absolute_url(self):
        return reverse("tutorial:lesson", kwargs={"lesson_id": self.pk})
