from django.shortcuts import get_object_or_404
from django.test import TestCase, Client, RequestFactory
from datetime import datetime

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient, APIRequestFactory
from .models import PollQuestion, PollChoice
from .serializers import PollQuestionListPageSerializer, PollQuestionDetailPageSerializer
from survey.servies import SurveyService
from survey.views import QuestionView, QuestionDetailView, VoteView


class TestSurveyView(APITestCase):

    def setUp(self):
        self.question1 = PollQuestion.objects.create(
            question_text='first question',
            pub_date=datetime.now()
        )
        self.choice1 = PollChoice.objects.create(
            question=self.question1,
            choice_text='yes',
        )
        self.choice1 = PollChoice.objects.create(
            question=self.question1,
            choice_text='no',
        )

        self.client = APIClient()
        self.factory = APIRequestFactory()

    def test_survey_questions_list(self):
        request = self.factory.get('questions_list')
        response = QuestionView.as_view({'get': 'list'})(request)
        serializer = PollQuestionListPageSerializer(PollQuestion.objects.all(), many=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_question_detail(self):
        request = self.factory.get('question_detail')
        response = QuestionDetailView.as_view({'get': 'retrieve'})(request, question_id=self.question1.id)
        question = PollQuestion.objects.get(id=self.question1.id)
        serializer = PollQuestionDetailPageSerializer(question)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)


class TestSurveyService(APITestCase, SurveyService):
    def setUp(self):
        self.question1 = PollQuestion.objects.create(
            question_text='first question',
            pub_date=datetime.now()
        )
        self.question2 = PollQuestion.objects.create(
            question_text='second question',
            pub_date=datetime.now()
        )

        self.choice1 = PollChoice.objects.create(
            question=self.question1,
            choice_text='yes',
        )
        self.choice1 = PollChoice.objects.create(
            question=self.question1,
            choice_text='no',
        )
        self.choice3 = PollChoice.objects.create(
            question=self.question2,
            choice_text='no',
        )

    def test_save_choice(self):
        result = self.save_choice(self.choice1.id, self.question1)
        self.choice1.votes += 1
        self.assertIn(result, PollChoice.objects.all())
        self.assertEqual(result.votes, self.choice1.votes)

    def test_get_question_by_id(self):
        result = self.get_question_by_id(self.question1.id, PollQuestionDetailPageSerializer)
        question = PollQuestion.objects.get(id=self.question1.id)
        serializer = PollQuestionDetailPageSerializer(question)
        self.assertEqual(result, serializer.data)

    def test_update_question_is_valid(self):
        data_choice = {
            "choice_id": self.choice1.id,
        }
        result, status = self.update_question(self.question1.id, data_choice)
        self.assertEqual(status, 200)

    def test_update_question_is_invalid(self):
        choice = self.choice3.id
        result, status = self.update_question(self.question1.id, choice)
        self.assertIn(status, range(400, 500))
