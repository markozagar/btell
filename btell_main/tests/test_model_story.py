from django import test
from django.contrib.auth import models as auth_models

from btell_main import models


class TestStoryModel(test.TestCase):

    def setUp(self):
        auth_models.User.objects.create(username='Someone')
    
    def test_new_story_is_not_published(self):
        user = auth_models.User.objects.get(username='Someone')
        story = models.Story(author=user, title='Great work of art', description='It really is.')

        self.assertFalse(story.is_published())

    def test_story_is_published_after_publish(self):
        user = auth_models.User.objects.get(username='Someone')
        story = models.Story(author=user, title='Great work of art', description='It really is.')

        story.publish()
        self.assertTrue(story.is_published())
