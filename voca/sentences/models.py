from django.db import models
from .fields import Category, LangISO
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
import uuid


class Sentence(models.Model):
    ref_id = models.UUIDField(default=uuid.uuid4, editable=False)
    sentence_length = models.FloatField(default=0)
    avg_word_length = models.FloatField(default=0)
    reports = models.IntegerField(default=0)
    language = models.TextField(choices=LangISO.choices)
    content = models.CharField(max_length=255)
    source = models.CharField(max_length=255, blank=True)
    category = models.TextField(choices=Category.choices, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['language']),
        ]


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
