"""Models for the BTell webpage."""
import datetime

from django.db import models
from django.db.models import signals
from django.utils import timezone
from django.contrib.auth import models as auth_models
from django import dispatch


class Profile(models.Model):
    """Extension to the basic User model which adds some more fields we use in BTell."""
    user = models.OneToOneField(auth_models.User, on_delete=models.CASCADE)
    # We will default this to the string 'DEFAULT', which implies we should pick from
    # whatever the site-administrator has configured as the default theme.
    theme = models.CharField(verbose_name='website_theme',
                             max_length=100, default='DEFAULT')

    @dispatch.receiver(signals.post_save, sender=auth_models.User)
    def create_user_profile(sender: 'Profile', instance: auth_models.User, created: bool, **kwargs):  # pylint:disable=no-self-argument
        """Called when a new user is created, so we can attach a default profile."""
        del kwargs
        if created:
            Profile.objects.create(user=instance)  # pylint:disable=no-member

    @dispatch.receiver(signals.post_save, sender=auth_models.User)
    def save_user_profile(sender: 'Profile', instance: auth_models.User, **kwargs):  # pylint:disable=no-self-argument
        """Called when a user object is saved, so we can make sure any changes to the profile are saved."""
        del kwargs
        instance.profile.save()  # type: ignore

    @staticmethod
    def profile_from_user(user: auth_models.User) -> 'Profile':
        """Loads the profile from a given user.

        We expect each registered user to have an associated profile with their settings.
        This should have been done by the `receiver` hooks in this model. If that mechanism
        failed, (e.g. if a user was created manually in the database), this function will
        emit a warning and create a default profile to associate with the user.
        """
        try:
            if isinstance(user.profile, Profile):  # type: ignore
                profile: 'Profile' = user.profile  # type: ignore
                return profile
        except auth_models.User.profile.RelatedObjectDoesNotExist:  # type:ignore pylint:disable=no-member
            # This is what we know how to handle, but we want
            # to let other types of errors flow upwards to Django.
            pass

        # If we came here profile doesn't exist, or is the wrong type.
        profile = Profile()
        user.profile = profile  # type: ignore
        profile.save()
        user.save()
        return profile

    def __str__(self):
        return f'Profile ({self.user.username})'  # pylint:disable=no-member


class SiteSettings(models.Model):
    """Site-specific configuration which applies to all users."""
    # Theme, selected by setting a different CSS file for web templates.
    default_theme = models.CharField(max_length=100)


class Tags(models.Model):
    """List of all known tags."""
    tag_name = models.CharField(max_length=40)


class Comment(models.Model):
    """Stores all comments published to the webpage."""
    commenter = models.ForeignKey(auth_models.User, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=1000)


class Story(models.Model):
    """Represents a single story."""
    author = models.ForeignKey(auth_models.User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=False)
    published = models.DateTimeField(null=True)  # If null, story is not published.
    last_update = models.DateTimeField(
        null=False, default=timezone.now)
    # Cover image file will be a sha256 hash (hex) from a specified uploads directory.
    cover_image_file = models.CharField(max_length=32, null=True)
    # A link to where the cover image is from, if applicable.
    cover_image_source = models.CharField(max_length=500, null=True)
    description = models.CharField(max_length=2000, null=False)
    tags = models.ManyToManyField(to=Tags)
    comments = models.ManyToManyField(to=Comment)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)

    def publish(self):
        """Publishes the story."""
        self.published = datetime.datetime.now(tz=datetime.timezone.utc)
        self.save()

    def is_published(self):
        """Returns `True` if the story is published or `False` if it's a draft."""
        return self.published is not None


class Chapter(models.Model):
    """A single chapter in some story."""
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=False)
    # Simplified story markdown
    content = models.TextField()
    published = models.DateTimeField(null=True)  # If null, chapter is not published
    last_update = models.DateTimeField(null=False, default=datetime.datetime.utcnow)
    chapter_image = models.CharField(max_length=32, null=True)
    chapter_image_source = models.CharField(max_length=500, null=True)


class ChapterLink(models.Model):
    """CYOA links between chapters."""
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    from_chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    to_chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='+')
    text = models.CharField(max_length=50, null=False)
    # Expressed with story DSL.
    condition = models.CharField(max_length=500, null=True)
    action = models.CharField(max_length=500, null=True)


class StoryReader(models.Model):
    """Stores the state of someone reading some story.

    Note: This is only used for logged-in users to persist their reading state
    accross browsers and devices. Anonymous users do not get this feature, and
    their reading state is saved locally, on their browser.
    """
    user = models.ForeignKey(auth_models.User, on_delete=models.CASCADE)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    current_chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    last_updated = models.DateTimeField(null=False, default=datetime.datetime.utcnow)


class StoryReaderVars(models.Model):
    """List and values of story variables for a reader."""
    reader = models.ForeignKey(StoryReader, on_delete=models.CASCADE)
    variable_name = models.CharField(max_length=50, null=False)
    variable_value = models.SmallIntegerField(null=False, default=0)
