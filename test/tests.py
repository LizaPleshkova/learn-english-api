from datetime import datetime

from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate

from test.models import Category, Test, Question, Answer, TestResult, AnswerUser
from test.services import TestDetailService, SaveAnswerUserService, SubmitTestService
from test.views import TestListView, TestUserView, TestDetailView, SaveUserAnswer, CompletedTestView
from test.serializers import TestListSerializer, MyTestListSerializer, TestDetailSerializer

User = get_user_model()


class TestViewTest(APITestCase):

    def setUp(self) -> None:
        self.user1 = User.objects.create(username='first', password='147123')
        self.user2 = User.objects.create(username='second', password='123147')

        self.user1_token = Token.objects.create(user=self.user1)
        self.user2_token = Token.objects.create(user=self.user2)

        self.category = Category.objects.create(
            title='Category for testing'
        )
        self.test1 = Test.objects.create(
            title='Test1',
            category_id=self.category,
            date_published=datetime.now()
        )
        self.test2 = Test.objects.create(
            title='Test2',
            category_id=self.category,
            date_published=datetime.now()
        )

        self.question1 = Question.objects.create(
            title='it\'s question1',
            test_id=self.test1
        )
        self.question2 = Question.objects.create(
            title='it\'s question2',
            test_id=self.test1
        )
        self.question3 = Question.objects.create(
            title='it\'s question3',
            test_id=self.test2
        )

        self.answer1_1 = Answer.objects.create(
            title='yes',
            question_id=self.question1,
            is_correct=True,
            points=5
        )
        self.answer1_2 = Answer.objects.create(
            title='no',
            question_id=self.question1,
            is_correct=False,
            points=0
        )
        self.answer2_1 = Answer.objects.create(
            title='yes',
            question_id=self.question2,
            is_correct=True,
            points=5
        )
        self.answer3_1 = Answer.objects.create(
            title='yes',
            question_id=self.question3,
            is_correct=True,
            points=5
        )
        self.factory = APIRequestFactory()

    def test_get_test_list(self):
        request = self.factory.get('test-list')
        force_authenticate(request, user=self.user1, token=self.user1_token)
        response = TestListView.as_view()(request)
        question = Test.objects.all()
        serializer = TestListSerializer(question, many=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_get_test_list_user(self):
        request = self.factory.get('test-user')
        force_authenticate(request, user=self.user1, token=self.user1_token)

        response = TestUserView.as_view()(request)

        question = Test.objects.filter(test__user=self.user1)
        serializer = MyTestListSerializer(question, many=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_get_detail_test(self):
        view = TestDetailView.as_view()
        request = self.factory.get('test-detail')
        force_authenticate(request, user=self.user1, token=self.user1_token)
        response = view(request, test_id=self.test1.id)
        response.render()

        question = Test.objects.get(id=self.test1.id)
        serializer = TestDetailSerializer(question)

        self.assertEqual(len(TestResult.objects.all()), 1)
        self.assertEqual(response.status_code, 200)

    def test_save_answer_user(self):
        self.testres1 = TestResult.objects.create(user=self.user1, test=self.test1)
        self.answer_user1 = AnswerUser.objects.create(test_result=self.testres1, question=self.question1)
        self.answer_user2 = AnswerUser.objects.create(test_result=self.testres1, question=self.question2)
        data = {
            'test_result': self.testres1.id,
            'question': self.question1.id,
            'answer': self.answer1_1.id,
        }
        view = SaveUserAnswer.as_view()
        request = self.factory.patch('save-answer', data, format='json')
        force_authenticate(request, user=self.user1, token=self.user1_token)
        response = view(request)

        response.render()
        self.assertEqual(response.status_code, 200)

    def test_get_completed_user_test(self):
        'completed-test'
        request = self.factory.get('completed-test')
        force_authenticate(request, user=self.user1, token=self.user1_token)

        view = CompletedTestView.as_view()
        request = self.factory.get('completed-test')
        force_authenticate(request, user=self.user1, token=self.user1_token)
        response = view(request)

        response.render()
        self.assertEqual(response.status_code, 200)


class TestServiceTest(APITestCase, TestDetailService, SaveAnswerUserService, SubmitTestService):
    def setUp(self) -> None:
        self.user1 = User.objects.create(username='first', password='147123')
        self.user2 = User.objects.create(username='second', password='123147')

        self.user1_token = Token.objects.create(user=self.user1)
        self.user2_token = Token.objects.create(user=self.user2)

        self.category = Category.objects.create(title='Category for testing')
        self.test1 = Test.objects.create(
            title='Test1',
            category_id=self.category,
            date_published=datetime.now()
        )
        self.test2 = Test.objects.create(
            title='Test2',
            category_id=self.category,
            date_published=datetime.now()
        )

        self.question1 = Question.objects.create(
            title='it\'s question1',
            test_id=self.test1
        )
        self.question2 = Question.objects.create(
            title='it\'s question2',
            test_id=self.test1
        )
        self.question3 = Question.objects.create(
            title='it\'s question3',
            test_id=self.test2
        )

        self.answer1_1 = Answer.objects.create(
            title='yes',
            question_id=self.question1,
            is_correct=True,
            points=0
        )
        self.answer1_2 = Answer.objects.create(
            title='no',
            question_id=self.question1,
            is_correct=False,
            points=5
        )
        self.answer2_1 = Answer.objects.create(
            title='yes',
            question_id=self.question2,
            is_correct=True,
            points=5
        )
        self.answer3_1 = Answer.objects.create(
            title='yes',
            question_id=self.question3,
            is_correct=True,
            points=5
        )
        self.testres1 = TestResult.objects.create(
            user=self.user1,
            test=self.test1
        )

        self.answer_user1 = AnswerUser.objects.create(
            test_result=self.testres1,
            question=self.question1
        )

        self.testres2 = TestResult.objects.create(
            user=self.user1,
            test=self.test2,
            completed=True,
            score=10.0
        )
        self.testres3 = TestResult.objects.create(
            user=self.user2,
            test=self.test2,
            completed=True,
            score=10.0
        )

        self.answer_user1 = AnswerUser.objects.create(
            test_result=self.testres2,
            question=self.question3
        )
        self.factory = APIRequestFactory()

    def test_get_or_create_test_result(self):
        ''' for TestDetailService.get_or_create_test_result, when testresult created '''

        self.assertEqual(len(TestResult.objects.all()), 3)

        result, status = self.get_or_create_test_result(self.user2, self.test1)

        self.assertEqual(len(TestResult.objects.all()), 4)
        self.assertEqual(status, 200)

    def test_save_answer_user(self):
        data = SaveAnswerUserService.save_answer_user(self.testres1, self.question1, self.answer1_1)
        self.assertEqual(data.answer, self.answer1_1)

    def test_update_user_answer(self):
        data, status = self.update_user_answer(self.testres1, self.answer1_1, self.question1)
        self.assertEqual(status, 200)

    def test_update_user_answer_invalid(self):
        ''' when test is completed '''
        data, status = self.update_user_answer(self.testres2, self.answer3_1, self.question3)
        self.assertEqual(status, 412)

    def test_save_test_result_invalid(self):
        ''' when test is completed -> 412'''
        self.dataa = AnswerUser.objects.create(
            test_result=self.testres3,
            question=self.question3,
            answer=self.answer3_1
        )
        data, status = self.save_test_result(self.user2, self.testres3, self.question3, self.answer3_1, self.test2)
        self.assertEqual(status, 412)

    def test_save_test_result_valid(self):
        ''' when test isn't completed -> 200'''
        self.answer_user2 = AnswerUser.objects.create(
            test_result=self.testres1,
            question=self.question2,
            answer=self.answer2_1,
        )
        data, status = self.save_test_result(self.user1, self.testres1, self.question2, self.answer2_1, self.test1)

        self.assertEqual(status, 200)
        self.assertEqual(self.testres1.completed, True)

    def test_count_score_user_test(self):
        # print('testres1', self.testres1, self.testres1.completed, self.testres1.score)
        self.assertEqual(self.testres1.completed, False)
        self.answer_user2 = AnswerUser.objects.create(
            test_result=self.testres1,
            question=self.question2,
            answer=self.answer2_1,
        )
        correct_answer, score = self.count_score_user_test(self.testres1)

        self.assertEqual(self.answer_user1.answer, None)

        self.assertEqual(correct_answer, 1)
        self.assertEqual(score, 5)
