from django import test
from django.contrib.auth import models as auth_models

from btell_main import models

class TestProfileRetrieve(test.TestCase):

    def setUp(self):
        auth_models.User.objects.create(username='some_user')
    
    def test_user_has_profile(self):
        user = auth_models.User.objects.get(username='some_user')
        profile = models.Profile.profile_from_user(user)
        self.assertIsNotNone(profile)
    
    def test_generate_default_profile(self):
        user = auth_models.User.objects.create(username='other_user')
        profile: models.Profile = user.profile  # type: ignore
        user.profile = None  # type: ignore
        profile.delete()

        profile = models.Profile.profile_from_user(user)
        self.assertIsNotNone(profile)