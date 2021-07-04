from django.urls import path
from survey.views import QuestionView, QuestionDetailView, VoteView, ResultView

urlpatterns = [
    path('questions/', QuestionView.as_view({'get': 'list'}), name='questions_list'),
    path('questions/<int:question_id>/', QuestionDetailView.as_view({'get': 'retrieve'}), name='question_detail'),
    path('questions/<int:question_id>/vote/', VoteView.as_view({'patch': 'partial_update'}), name='vote'),
    path('questions/<int:question_id>/result/', ResultView.as_view({'get': 'list'}), name='question_result'),
]
