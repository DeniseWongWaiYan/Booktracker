from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    date_of_birth = models.DateField(blank=True, null=True)
    profile_picture = ImageField(upload_to='users/%d/%m/%y', blank=True, null=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)
    

class Connection(models.Model):
    user_to = models.ForeignKey(User, related_name='rel_to_set')
    user_from = models.ForeignKey(User, related_name='rel_from_set')
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{} followed {}'.format(self.user_from, self.user_to)


User.add_to_class('following', models.ManyToManyField('self', through=Connection, related_name='followers', symmetrical=False))

#


