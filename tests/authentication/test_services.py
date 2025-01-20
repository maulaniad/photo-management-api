from datetime import timedelta
from decouple import config
from freezegun import freeze_time
from jwt import decode, ExpiredSignatureError

from django.conf import settings
from django.core.mail import outbox
from django.utils.timezone import now

from api.authentication.services import AuthService

from tests import APITestCase
from tests.authentication.fixtures import AUTHENTICATION_FIXTURES
from unittest.mock import patch


class TestAuthenticationServices(APITestCase):
    fixtures = AUTHENTICATION_FIXTURES

    def setUp(self) -> None:
        settings.EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

        self.service = AuthService
        self.patcher = patch("celery.app.task.Task.delay")
        self.mock_celery = self.patcher.start()
        return super().setUp()

    def tearDown(self) -> None:
        outbox.clear()
        return super().tearDown()

    def test_token_should_expire(self):
        settings.OTP_AUTH = False

        token, _ = self.service.login(
            {
                'username': config('TEST_USERNAME', default=None, cast=str),
                'password': config('TEST_PASSWORD', default=None, cast=str)
            }
        )

        with freeze_time(now() + timedelta(hours=settings.JWT_EXP_HOURS)):
            try:
                decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
                expired = False
            except ExpiredSignatureError:
                expired = True

        self.assertTrue(expired, msg="Token should be able to expire")

    def test_otp_should_be_created(self):
        settings.OTP_AUTH = True

        access_id, _ = self.service.create_otp(
            {
                'username': config('TEST_USERNAME', default=None, cast=str),
                'password': config('TEST_PASSWORD', default=None, cast=str)
            }
        )

        self.assertIsNotNone(access_id, msg="OTP should be created")

    def test_otp_should_not_exceed_max_retries(self):
        settings.OTP_AUTH = True

        access_id, _ = self.service.create_otp(
            {
                'username': config('TEST_USERNAME', default=None, cast=str),
                'password': config('TEST_PASSWORD', default=None, cast=str)
            }
        )

        for _ in range(settings.OTP_MAX_RETRIES):
            access_id, _ = self.service.verify_otp(
                {
                    'access_id': access_id,
                    'otp': 12300
                }
            )

        self.assertIsNone(access_id, msg="OTP should not exceed max retries")

    def test_otp_mail_should_be_sent(self):
        settings.OTP_AUTH = True

        access_id, _ = self.service.create_otp(
            {
                'username': config('TEST_USERNAME', default=None, cast=str),
                'password': config('TEST_PASSWORD', default=None, cast=str)
            }
        )

        self.assertEqual(len(outbox), 1, msg="OTP mail should be sent")
        self.assertIn(access_id, str(outbox[0].body), msg="OTP should be in email body")
