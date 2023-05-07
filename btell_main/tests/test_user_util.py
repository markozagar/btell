import logging

from django import test, http
from django.contrib.auth import models as auth_models
from btell_main.util import user_util

class GenerateRandomPasswordTest(test.TestCase):

    def test_random_pass_is_correct_length(self):
        pw1 = user_util.generate_random_password(8)
        self.assertEqual(len(pw1), 8)

        pw2 = user_util.generate_random_password(12)
        self.assertEqual(len(pw2), 12)

class GetUserObjectTest(test.TestCase):

    def setUp(self):
        auth_models.User.objects.create(username='someuser')

    def test_returns_none_if_not_auth(self):
        request = http.HttpRequest()
        request.user = auth_models.AnonymousUser()
        user = user_util.get_user_object(request)
        self.assertIsNone(user)
    
    def test_returns_user_from_db(self):
        """
        This test doesn't tell us a whole lot, but it should confirm
        that `get_user_object()` correctly checks the model type.
        """
        request = http.HttpRequest()
        request.user = auth_models.User.objects.get(username='someuser')
        user = user_util.get_user_object(request)
        self.assertIsNotNone(user)
        if user:
            self.assertEqual(user.username, 'someuser')
    
    def test_returns_none_if_wrong_type(self):
        class WrongUserType:
            def __init__(self):
                self.is_authenticated = True

        request = http.HttpRequest()
        request.user = WrongUserType()  # type: ignore
        # Disable warn log output when doing this.
        logging.disable(logging.CRITICAL)
        user = user_util.get_user_object(request)
        logging.disable(logging.INFO)
        self.assertIsNone(user)
