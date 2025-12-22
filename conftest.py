from django.test.client import Client
import pytest
from core.models import CustomUser as User
from django.contrib.auth.hashers import make_password

@pytest.fixture
def client():
    return Client()

@pytest.fixture # provides a test user instance
def user_instance(db):
    return User.objects.create_user(username="testuser", email="testuser@example.com", password="testpassword123")

@pytest.fixture
def auth_user_password() -> str:
    return "testpassword123"

