from rest_framework import serializers

from survey.models import PollQuestion, PollChoice


class PollQuestionListPageSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    question_text = serializers.CharField(max_length=200)
    pub_date = serializers.DateTimeField()

    def create(self, validated_data):
        return PollQuestion.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class PollChoiceSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    choice_text = serializers.CharField(max_length=200)

    def create(self, validated_data):
        return PollChoice.objects.create(**validated_data)


class PollQuestionDetailPageSerializer(PollQuestionListPageSerializer):
    choices = PollChoiceSerializer(many=True, read_only=True)


class VoteSerializer(serializers.Serializer):
    choice_id = serializers.IntegerField()


class ChoiceSerializerWithVotes(PollChoiceSerializer):
    votes = serializers.IntegerField(read_only=True)


class QuestionResultPageSerializer(PollQuestionListPageSerializer):
    choices = ChoiceSerializerWithVotes(many=True, read_only=True)
