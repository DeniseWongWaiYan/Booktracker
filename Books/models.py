from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.core.urlresolvers import reverse
from sorl.thumbnail import ImageField
from django.contrib.auth.models import User



# Create your models here.
    
class Books(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    ISBN = models.IntegerField(error_messages={})
    users_like=models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='books_liked', blank=True)
    slug = models.SlugField(max_length=200, blank=True)
 #  total_likes = models.PositiveIntegerField(db_index=True)
    coverpic = models.ImageField(upload_to='books/%Y/%m/%d', blank=True, null=True)


    def __str__(self):
        
        return '{} was written by {} and has ISBN number {} with {} likes'.format(self.title, self.author, self.ISBN, self.users_like.count(),)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            super(Books, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('Books:detail', args=[self.slug, self.ISBN])

class BookPicture(models.Model):
    book = models.OneToOneField(Books)
    originalcoverpic  = models.ImageField(upload_to='books/%Y/%m/%d', blank=True, null=True)


class Review(models.Model):
    book = models.ForeignKey(Books, related_name='reviews')
    body = models.TextField()
    commenter = models.ForeignKey(User, related_name='commenter')
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.commenter, self.created)

class Challenge(models.Model):
    chalname = models.CharField(max_length=200)
    bookinchallenge = models.ManyToManyField(Books)


