from django.urls import path

from test.views import TestListView, TestUserView, TestDetailView, SaveUserAnswer, \
    SubmitTestView, CompletedTestView

urlpatterns = [
    path('test-list/', TestListView.as_view(), name='test-list'),
    path("my-tests/", TestUserView.as_view(), name='test-user'),
    path('test-detail/<int:test_id>/', TestDetailView.as_view(), name='test-detail'),
    path('save-answer/', SaveUserAnswer.as_view(), name='save-answer'),
    path("<int:test_id>/submit/", SubmitTestView.as_view(), name='submit-test'),
    path("completed-test/", CompletedTestView.as_view(), name='completed-test'),
]
