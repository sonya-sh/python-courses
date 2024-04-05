import os
from django.conf import settings
import pytest
from django.contrib.auth.models import Group
from django.test import Client
from django.contrib.auth import get_user_model

os.environ["DJANGO_SETTINGS_MODULE"] = "online_school.settings"

CustomUser = get_user_model()

@pytest.fixture
def create_customuser_group():
    return Group.objects.create(name='TestGroup')

@pytest.fixture
def create_custom_user(create_customuser_group):
    return CustomUser.objects.create_user(
        first_name='testname',
        last_name='testsur',
        email='test@mail.ru',
        phone='1234567',
        customuser_group=create_customuser_group,
        password='us1passwd'
    )

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def authenticate(client, create_custom_user):
    user = create_custom_user
    client.login(username=user.email, password='us1passwd')
    return client
