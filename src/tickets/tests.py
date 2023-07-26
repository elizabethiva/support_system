from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from tickets.models import Ticket
from users.serializers import UserCreateSerializer

User = get_user_model()


class TicketsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.payload = {
            "email": "john@email.com",
            "password": "@Dm1n#LKJ",
        }
        cls.default_client_payload = {
            "follow": True,
            "content_type": "application/json",
        }
        serializer = UserCreateSerializer(data=cls.payload)
        serializer.is_valid()
        cls.user = serializer.save()
        cls.client = Client(
            HTTP_CONTENT_TYPE="application/json",
        )

    def testUsersNumber(self):
        total_users = User.objects.count()
        assert total_users == 1

    def _authorize(self) -> str:
        response = self.client.post(
            "/auth/token/", self.payload, **self.default_client_payload
        )

        return response.json()["access"]

    def testTicketCreate(self):
        token: str = self._authorize()
        self.client.post(
            "/tickets",
            HTTP_AUTHORIZATION=f"Bearer {token}",
            data={
                "title": "gog created ticket Nullam mollis.",
                "text": "Vestibulum vel ",
            },
            **self.default_client_payload,
        )

        assert Ticket.objects.count() == 1