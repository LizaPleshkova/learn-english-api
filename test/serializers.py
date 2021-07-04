from rest_framework import serializers
from django.contrib.auth.models import User

from test.models import Category, Test, Question, Answer, AnswerUser, TestResult


class MyTestListSerializer(serializers.ModelSerializer):
    completed = serializers.SerializerMethodField()
    questions_count = serializers.SerializerMethodField()
    score = serializers.SerializerMethodField()

    class Meta:
        model = Test
        fields = ["id", "title", "questions_count", "completed", "score"]
        read_only_fields = ["questions_count", "completed"]

    def get_completed(self, obj):
        try:
            test_res = TestResult.objects.get(user=self.context['request'].user, test=obj)
            return test_res.completed
        except TestResult.DoesNotExist:
            return None

    def get_questions_count(self, obj):
        return obj.questions.all().count()

    def get_score(self, obj):
        try:
            test_res = TestResult.objects.get(user=self.context['request'].user, test=obj)
            if test_res.completed == True:
                return test_res.score
            return None
        except TestResult.DoesNotExist:
            return None


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'url', 'username', 'email', 'is_staff']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TestListSerializer(serializers.ModelSerializer):
    questions_count = serializers.SerializerMethodField()

    class Meta:
        model = Test
        fields = ('id', 'title', 'questions_count')
        read_only_fields = ["questions_count"]

    def get_questions_count(self, obj):
        return obj.questions.all().count()


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ["id", "title", "is_correct", "points"]


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ('title', 'answers')


class AnswerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerUser
        fields = ('test_result', 'question', 'answer')


class TestResultSerializer(serializers.ModelSerializer):
    answers_user = AnswerUserSerializer(many=True)

    class Meta:
        model = TestResult
        fields = ('id', 'test', 'score', 'completed', 'answers_user')


class TestDetailSerializer(serializers.ModelSerializer):
    test_result = serializers.SerializerMethodField()
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Test
        fields = ('id', 'test_result', 'questions')

    def get_test_result(self, obj):
        try:
            test_res = TestResult.objects.get(user=self.context['user'], test=obj)
            serializer = TestResultSerializer(test_res)
            return serializer.data
        except TestResult.DoesNotExist:
            return None


class FinalTestResultSerializer(serializers.ModelSerializer):
    test_result = serializers.SerializerMethodField()
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Test
        fields = "__all__"

    def get_test_result(self, obj):
        try:
            test_result = TestResult.objects.get(user=self.context["user"], test=obj)
            serializer = TestResultSerializer(test_result)
            print(serializer.data)
            return serializer.data
        except TestResult.DoesNotExist:
            return None
