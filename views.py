from datetime import date

from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView

from consultants.auth import ExpiringTokenAuthentication
from polls.models import Polls, PollsResults
from polls.serializers import PollsListSerializer, PollsResultsSerializer
from utils.client import decorAnonymusReturn401Serializer


class GetPollById(RetrieveAPIView):

    queryset = Polls.objects
    serializer_class = PollsListSerializer


class GetActivePolls(ListAPIView):
    """
    Отдает список голосований, исходя из условий
    1) Дата старта >= сегодня
    2) Дата конца <= сегодня
    3) У консультанта нет результатов по этому голосованию
    """
    serializer_class = PollsListSerializer

    @decorAnonymusReturn401Serializer
    def get_queryset(self):
        today = date.today()
        return Polls.objects.filter(
            date_end__gte=today, date_start__lte=today
        ).exclude(
            polls_results__consultant=self.request.user.id
        )


class ResultPollFromConsultant(CreateAPIView):
    authentication_classes = [ExpiringTokenAuthentication]
    queryset = PollsResults.objects
    serializer_class = PollsResultsSerializer

    @decorAnonymusReturn401Serializer
    def perform_create(self, serializer):
        serializer.save(consultant=self.request.user)
