import json
from django.test import TestCase, Client
from .models import User
from django.contrib.auth import get_user_model

client = Client()


class RegisterTest(TestCase):
    def setUp(self):
        self.User = get_user_model()

    def test_register_post_success(self):
        register_info = {
            "email": "test@test.io",
            "name": "test",
            "password1": "qwer123!!!",
            "password2": "qwer123!!!",
            "is_korean": 0,
        }
        response = client.post(
            "/api/v1/user/register/",
            json.dumps(register_info),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)

    def test_register_post_invalid_password(self):
        register_info = {
            "email": "test@test.io",
            "name": "test",
            "password1": "1234567",
            "password2": "1234567",
            "is_korean": 1,
        }
        response = client.post(
            "/api/v1/user/register/",
            json.dumps(register_info),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_register_post_invalid_email(self):
        register_info = {
            "email": "test@testio",
            "name": "test",
            "password1": "test123!!!",
            "password2": "test123!!!",
            "is_korean": 1,
        }
        response = client.post(
            "/api/v1/user/register/",
            json.dumps(register_info),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
