from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.authtoken.admin import User
from rest_framework import viewsets, permissions, generics
from rest_framework.permissions import IsAuthenticated

from test.serializers import TestListSerializer, MyTestListSerializer, TestResultSerializer, \
    UserSerializer, TestDetailSerializer, AnswerUserSerializer, FinalTestResultSerializer

from test.models import Test, Question, Answer, TestResult

from test.services import TestDetailService, SaveAnswerUserService, SubmitTestService


# 1
class TestListView(generics.ListAPIView):
    ''' for the output all tests'''
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TestListSerializer
    queryset = Test.objects.all()


class TestUserView(generics.ListAPIView):
    ''' for the output all the user's tests '''
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = MyTestListSerializer

    def get_queryset(self, *args, **kwargs):
        queryset = Test.objects.filter(test__user=self.request.user)
        return queryset


class CompletedTestView(generics.ListAPIView):
    ''' for the output user's completed tests'''
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = TestResultSerializer

    def get_queryset(self, *args, **kwargs):
        queryset = TestResult.objects.filter(user=self.request.user, completed=True)
        return queryset


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)


class TestResultDetailList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = TestDetailSerializer
    queryset = Test.objects.all()


# 2
class TestDetailView(generics.RetrieveAPIView, TestDetailService):
    ''' for the output user's test by test_id'''
    serializer_class = TestDetailSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, *args, **kwargs):
        test = self.kwargs.get('test_id')
        test = get_object_or_404(Test, id=test)
        returns, status = self.get_or_create_test_result(self.request.user, test)
        return Response(returns, status=status)


class SaveUserAnswer(generics.UpdateAPIView, SaveAnswerUserService):
    serializer_class = AnswerUserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def patch(self, request, *args, **kwargs):
        test_result_id = self.request.data.get('test_result')
        question_id = request.data.get('question')
        answer_id = request.data.get('answer')

        test_result = get_object_or_404(TestResult, user=self.request.user, id=test_result_id)
        question = get_object_or_404(Question, id=question_id)
        answer = get_object_or_404(Answer, id=answer_id)

        returns, status = self.update_user_answer(test_result=test_result, answer=answer, question=question)

        return Response(returns, status=status)


class SubmitTestView(generics.GenericAPIView, SubmitTestService):
    serializer_class = FinalTestResultSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def post(self, request, *args, **kwargs):
        test_result_id = request.data.get('test_result')
        question_id = request.data.get('question')
        answer_id = request.data.get('answer')

        test_result = get_object_or_404(TestResult, id=test_result_id)
        question = get_object_or_404(Question, id=question_id)
        test = Test.objects.get(id=self.kwargs.get('test_id'))
        answer = get_object_or_404(Answer, id=answer_id)

        data, status = self.save_test_result(self.request.user, test_result, question, answer, test)
        return Response(data, status=status)
