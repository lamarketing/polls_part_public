from django.urls import path
from polls.views import GetPollById, GetActivePolls, ResultPollFromConsultant

urlpatterns = [
    path('poll/<int:pk>', GetPollById.as_view()),
    path('get-active', GetActivePolls.as_view()),
    path('create-result', ResultPollFromConsultant.as_view()),
]
