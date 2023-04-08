import datetime

from django.db import models
from django.db.models import signals
from django.contrib.auth import models as auth_models
from django import dispatch


# Create your models here.


class Profile(models.Model):
    """Extension to the basic User model which adds some more fields we use in BTell."""
    user = models.OneToOneField(auth_models.User, on_delete=models.CASCADE)
    # We will default this to the string 'DEFAULT', which implies we should pick from
    # whatever the site-administrator has configured as the default theme.
    theme = models.CharField(verbose_name='website_theme',
                             max_length=100, default='DEFAULT')

    @dispatch.receiver(signals.post_save, sender=auth_models.User)
    def create_user_profile(sender: 'Profile', instance: auth_models.User, created: bool, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @dispatch.receiver(signals.post_save, sender=auth_models.User)
    def save_user_profile(sender: 'Profile', instance: auth_models.User, **kwargs):
        instance.profile.save()  # type: ignore

    def __str__(self):
        return f'Profile ({self.user.username})'


class SiteSettings(models.Model):
    """Site-specific configuration which applies to all users."""
    # Theme, selected by setting a different CSS file for web templates.
    default_theme = models.CharField(max_length=100)


class Tags(models.Model):
    tag_name = models.CharField(max_length=40)


class Comment(models.Model):
    commenter = models.ForeignKey(
        to=auth_models.User, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=1000)


class Story(models.Model):
    author = models.ForeignKey(auth_models.User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=False)
    published = models.DateTimeField(
        null=False, default=datetime.datetime.utcnow)
    last_update = models.DateTimeField(
        null=False, default=datetime.datetime.utcnow)
    # Cover image file will be a sha256 hash (hex) from a specified uploads directory.
    cover_image_file = models.CharField(max_length=32, null=True)
    # A link to where the cover image is from, if applicable.
    cover_image_source = models.CharField(max_length=500, null=True)
    description = models.CharField(max_length=2000, null=False)
    tags = models.ManyToManyField(to=Tags)
    comments = models.ManyToManyField(to=Comment)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    draft = models.BooleanField(default=True)
