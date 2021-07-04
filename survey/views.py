from rest_framework.response import Response
from rest_framework import status, viewsets

from survey.serializers import PollQuestionListPageSerializer, PollQuestionDetailPageSerializer, QuestionResultPageSerializer
from survey.models import PollQuestion
from survey.servies import SurveyService


class QuestionView(viewsets.ModelViewSet):
    queryset = PollQuestion.objects.all()
    serializer_class = PollQuestionListPageSerializer


class QuestionDetailView(viewsets.ModelViewSet, SurveyService):
    serializer_class = PollQuestionDetailPageSerializer

    def get_queryset(self, *args, **kwargs):
        question = PollQuestion.objects.filter(id=self.kwargs["question_id"])
        return question

    def retrieve(self, request, *args, **kwargs):
        data = self.get_question_by_id(self.kwargs.get("question_id"), PollQuestionDetailPageSerializer)
        return Response(data, status=status.HTTP_200_OK)


class VoteView(viewsets.ModelViewSet, SurveyService):
    queryset = PollQuestion.objects.all()
    serializer_class = PollQuestionListPageSerializer

    def get_queryset(self, *args, **kwargs):
        question = PollQuestion.objects.filter(id=self.kwargs.get("question_id"))
        return question

    def partial_update(self, request, *args, **kwargs):
        returns, status = self.update_question(self.kwargs.get("question_id"), request.data)
        return Response(returns, status=status)


class ResultView(viewsets.ModelViewSet, SurveyService):
    serializer_class = QuestionResultPageSerializer

    def get_queryset(self, *args, **kwargs):
        question = PollQuestion.objects.filter(id=self.kwargs.get("question_id"))
        return question

    def get(self, *args, **kwargs):
        data = self.get_question_by_id(self.kwargs.get("question_id"), QuestionResultPageSerializer)
        return Response(data, status=status.HTTP_200_OK)
