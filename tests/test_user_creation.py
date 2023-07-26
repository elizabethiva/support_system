import pytest
from django.contrib.auth import get_user_model

from users.serializers import UserCreateSerializer

User = get_user_model()


@pytest.mark.django_db
def test_user_creation():
    payload = {
        "email": "john@email.com",
        "password": "@Dm1n#LKJ",
    }
    serializer = UserCreateSerializer(data=payload)
    serializer.is_valid()
    user = serializer.save()

    assert User.objects.count() == 1
    assert user.id == 1
    assert user.email == payload["email"]