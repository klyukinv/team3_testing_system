from rest_framework import serializers
from exam.models import ExamSession


class ExamSessionAPISerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = ExamSession.objects.create(start=validated_data['start'], finsih=validated_data['finish'],
                                          stream=validated_data['stream'])
        return user

    class Meta:
        model = ExamSession
        fields = [
            'start',
            'finish',
            'stream',
        ]


class ExamSessionSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        instance.start = validated_data.get('start', instance.start)
        instance.finish = validated_data.get('finish', instance.finish)
        instance.stream = validated_data.get('stream', instance.stream)
        instance.save()
        return instance

    class Meta:
        model = ExamSession
        fields = [
            'start',
            'finish',
            'stream',
        ]