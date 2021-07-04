from datetime import datetime
from django.shortcuts import get_object_or_404
from rest_framework import status

from test.models import Question, Answer, TestResult, AnswerUser
from test.serializers import FinalTestResultSerializer, TestDetailSerializer, AnswerUserSerializer


class TestDetailService():

    def get_or_create_test_result(self, user, test):
        obj, created = TestResult.objects.get_or_create(user=user, test=test)
        if created:
            for question in Question.objects.filter(test_id=test.id):
                AnswerUser.objects.create(test_result=obj, question=question)
        else:
            last_question = self.get_last_question_test_user(obj)
        ser = TestDetailSerializer(test, context={'user': user})
        return ser.data, status.HTTP_200_OK

    def get_last_question_test_user(self, test_result):
        last_question = AnswerUser.objects.filter(test_result=test_result, answer__isnull=False)
        if last_question.count() > 0:
            return last_question.last().question.id
        else:
            return None


class SaveAnswerUserService():
    def save_answer_user(test_result, question, answer):
        obj = get_object_or_404(AnswerUser, question=question, test_result=test_result, )
        obj.answer = answer
        obj.save()
        return obj

    def update_user_answer(self, test_result, answer, question):
        if test_result.completed:
            return {"This hometask is already complete. You can't submit again"}, status.HTTP_412_PRECONDITION_FAILED
        obj = SaveAnswerUserService.save_answer_user(test_result=test_result, question=question, answer=answer)
        ser = AnswerUserSerializer(obj)
        return ser.data, status.HTTP_200_OK


class SubmitTestService():

    def save_test_result(self, user, test_res, question, answer, test):
        if test_res.completed:
            return {"This hometask is already complete. You can't submit again"}, status.HTTP_412_PRECONDITION_FAILED

        if answer.id is not None:
            SaveAnswerUserService.save_answer_user(test_result=test_res, question=question, answer=answer)

        test_res.completed = True
        test_res.count_correct, score = self.count_score_user_test(test_res)
        test_res.count_incorrect = test_res.test.questions.count() - test_res.count_correct
        test_res.score = score / test_res.test.questions.count()
        test_res.date_finished = datetime.now()
        test_res.save()
        serializer = FinalTestResultSerializer(test, context={'user': user})
        return serializer.data, status.HTTP_200_OK

    def count_score_user_test(self, test_result):
        correct_answers, score = 0, 0
        for users_answer in AnswerUser.objects.filter(test_result=test_result):
            answer = Answer.objects.get(question_id=users_answer.question, is_correct=True)
            if users_answer.answer == answer and users_answer.answer is not None:
                correct_answers += 1
                score += users_answer.answer.points

        return correct_answers, score
