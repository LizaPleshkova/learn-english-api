from django.urls import path
from hometask.views import HometaskView, HometaskUserList, HometaskList, \
    EvaluatedHometask, CompletedHometaskUser, SubmitHometask, UserProgressView

urlpatterns = [
    path('hometask/<int:hometask_id>/', HometaskView.as_view({'get': 'retrieve'}), name='hometask-user-detail'),
    path('hometask/', HometaskUserList.as_view({'get': 'list'}), name='hometask-user-list'),
    path('all-hometask/', HometaskList.as_view(), name='all-hometask-list'),
    path('evaluated-hometask/', EvaluatedHometask.as_view({'get': 'list'}), name='evaluated-hometask'),
    path('completed-hometask/', CompletedHometaskUser.as_view({'get': 'list'}), name='completed-hometask'),
    path('hometask/<int:hometask_id>/submit/', SubmitHometask.as_view(), name='hometask-submit'),
    path('', UserProgressView.as_view({'get': 'get'}), name='user-progress')
]
