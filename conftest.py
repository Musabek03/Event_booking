import pytest 
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .core.models import CustomUser

@pytest.fixture
def api_client():
    return APIClient


@pytest.fixture
def create_user(db):
    user = CustomUser.objects.create_user(username='testuser', password="testpassword123")
    return user
