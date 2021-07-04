from datetime import datetime
from django.shortcuts import get_object_or_404
from rest_framework import status

from hometask.serializers import HometaskSerializer, SubmitHometaskSerializer
from hometask.models import Hometask, CompletedHometask
from test.models import TestResult


class HometaskService():

    def get_serializer_data(self, user, hometask_id):
        queryset = get_object_or_404(Hometask, user=user, id=hometask_id)
        serializer = HometaskSerializer(queryset)
        return serializer.data

    def get_completed_task_or_create(self, hometask, file_txt):
        if file_txt is not None and file_txt != "":
            completed_task, created = CompletedHometask.objects.get_or_create(hometask=hometask)
            if created:
                self.create_completed_task(completed_task, hometask, file_txt)
            else:
                if completed_task.completed:
                    return {"This hometask is already complete. You can't submit again"}, status.HTTP_400_BAD_REQUEST
            serializer = SubmitHometaskSerializer(completed_task)
            return serializer.data, status.HTTP_200_OK
        else:
            return {"TThe file was not received. You can submit again"}, status.HTTP_412_PRECONDITION_FAILED

    def create_completed_task(self, completed_task, hometask, file_txt):
        completed_task.file_txt = file_txt
        completed_task.completed = True
        completed_task.date_finished = datetime.now()
        completed_task.save()


class UserProgressService():

    def _average_score_test(user):
        average_score_test = 0
        test_progress = TestResult.objects.filter(user=user, completed=True)
        for test_result in test_progress:
            average_score_test += test_result.score
        average_score_test = average_score_test / test_progress.count()
        return average_score_test

    def _average_score_hometask(user):
        average_score_hometask = 0
        hometask_progress = CompletedHometask.objects.filter(hometask__user=user, completed=True,
                                                             mark__isnull=False)
        for hometask in hometask_progress:
            average_score_hometask += hometask.mark
        average_score_hometask = average_score_hometask / hometask_progress.count()
        return average_score_hometask

    def average_score(user):
        average_score_hometask = UserProgressService._average_score_hometask(user)
        average_score_test = UserProgressService._average_score_test(user)
        return (average_score_test + average_score_hometask) / 2
