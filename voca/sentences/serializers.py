from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Sentence


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'id', 'password')
        write_only_fields = ('password',)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class SentenceSerializer(serializers.Serializer):
    content = serializers.CharField(max_length=120)
    sentence_length = serializers.FloatField()
    reports = serializers.IntegerField()
    avg_word_length = serializers.FloatField()
    language = serializers.CharField()
    id = serializers.UUIDField()
    category = serializers.CharField()

    def create(self, validated_data):
        return Sentence.objects.create(**validated_data)
