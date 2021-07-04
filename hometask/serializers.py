from rest_framework import serializers

from hometask.models import Hometask, CompletedHometask


class CompletedHometaskDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompletedHometask
        fields = ('id', 'file_txt', 'mark', 'comment_admin', "completed")


class HometaskSerializer(serializers.ModelSerializer):
    hometask = CompletedHometaskDetailSerializer(many=True)

    class Meta:
        model = Hometask
        fields = ('id', 'task', 'description', 'hometask')


class HometaskUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hometask
        fields = ('id', 'task', 'description')


class AllHometaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hometask
        fields = ('id', 'task', "description", "user")


class SubmitHometaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompletedHometask
        fields = "__all__"
