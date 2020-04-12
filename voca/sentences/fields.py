from django.db import models
from django.utils.translation import gettext_lazy as _


class DifficultyLevel(models.IntegerChoices):
    EASY = 0
    MODERATE = 1
    DIFFICULT = 2


class LangISO(models.TextChoices):
    DE = "de", _("German")
    EN = "en", _("English")
    ES = "es", _("Spanish")
    FR = "fr", _("French")


class Category(models.TextChoices):
    NEWS = "news", _("News")
    WEB = "web", _("Web")
    KIDS = "kids", _("Kids")
