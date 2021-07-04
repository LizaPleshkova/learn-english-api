from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, viewsets, status
from rest_framework.response import Response

from hometask.serializers import AllHometaskSerializer, HometaskUserSerializer, HometaskSerializer, SubmitHometaskSerializer
from hometask.models import Hometask
from test.serializers import FinalTestResultSerializer
from hometask.services import HometaskService, UserProgressService


class HometaskList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = AllHometaskSerializer
    queryset = Hometask.objects.all()


class HometaskUserList(viewsets.ModelViewSet):
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = HometaskUserSerializer

    def get_queryset(self, *args, **kwargs):
        queryset = Hometask.objects.filter(user=self.request.user)
        return queryset


class CompletedHometaskUser(viewsets.ModelViewSet):
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = HometaskSerializer

    def get_queryset(self, *args, **kwargs):
        queryset = Hometask.objects.filter(user=self.request.user, hometask__completed=True)
        return queryset


class EvaluatedHometask(viewsets.ModelViewSet):
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = HometaskSerializer

    def get_queryset(self, *args, **kwargs):
        queryset = Hometask.objects.filter(user=self.request.user, hometask__mark__isnull=False)
        return queryset


class SubmitHometask(generics.GenericAPIView, HometaskService):
    serializer_class = SubmitHometaskSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def post(self, request, *args, **kwargs):
        file_txt = request.data.get('file_txt')
        hometask = get_object_or_404(Hometask, user=self.request.user.id, id=self.kwargs.get("hometask_id"))
        data, status = self.get_completed_task_or_create(hometask, file_txt)
        return Response(data, status=status)


class HometaskView(viewsets.ViewSet, HometaskService):
    serializer_class = HometaskSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def retrieve(self, request, hometask_id=None):
        data = self.get_serializer_data(request.user.id, hometask_id)
        return Response(data, status=status.HTTP_200_OK)


class UserProgressView(viewsets.ViewSet, UserProgressService):
    serializer_class = FinalTestResultSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def get(self, *args, **kwargs):
        ''' get average score user's test and hometask'''
        avr_score = UserProgressService.average_score(self.request.user)
        return JsonResponse(
            {"average_score": avr_score}, safe=False, status=status.HTTP_200_OK)
