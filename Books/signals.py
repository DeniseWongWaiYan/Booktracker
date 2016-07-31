from __future__ import unicode_literals
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Books


@receiver(m2m_changed, sender=Books.users_like.through)
def users_like_changed(sender, instance, **kwargs):
    instance.total_likes = instance.authors.count()
    instance.save()
