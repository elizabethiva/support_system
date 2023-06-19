from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from tickets.models import Ticket
from tickets.serializers import TicketSerializer


class TicketAPIViewSet(ModelViewSet):
    model = Ticket
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]
