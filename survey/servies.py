from django.shortcuts import get_object_or_404
from rest_framework import status

from survey.models import PollQuestion, PollChoice
from survey.serializers import VoteSerializer


class SurveyService():

    def save_choice(self, choice_id: int, question: PollQuestion) -> None:
        choice = get_object_or_404(PollChoice, id=choice_id, question=question)
        choice.votes += 1
        choice.save()
        return choice

    def get_question_by_id(self, question_id: int, serializer_class, data=None):
        queryset = get_object_or_404(PollQuestion, id=question_id)

        if data is not None:
            serializer = serializer_class(queryset, data)
        else:
            serializer = serializer_class(queryset)
        return serializer.data

    def update_question(self, id, data):
        question = get_object_or_404(PollQuestion, id=id)
        serializer = VoteSerializer(data=data)

        if serializer.is_valid():
            self.save_choice(serializer.validated_data['choice_id'], question)
            return "voted", status.HTTP_200_OK
        else:
            return serializer.errors, status.HTTP_400_BAD_REQUEST
