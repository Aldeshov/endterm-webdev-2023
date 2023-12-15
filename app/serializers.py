import random

from rest_framework import serializers
from django.contrib.auth.models import User
from app.models import Post


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name')


class PostSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    text = serializers.CharField()
    author = UserSerializer(read_only=True)
    code = serializers.IntegerField(read_only=True)
    dateOfCreation = serializers.DateTimeField(read_only=True)

    def update(self, instance, validated_data):
        # Update the instance only if the respective fields are present in validated_data
        if 'title' in validated_data:
            instance.title = validated_data['title']
        if 'text' in validated_data:
            instance.text = validated_data['text']

        # Save the instance after making the changes
        instance.save()

        # Return the updated instance
        return instance

    def create(self, validated_data):
        code = random.randint(11111111, 99999999)
        while Post.objects.filter(code=code):
            code = random.randint(11111111, 99999999)

        validated_data.setdefault('code', code)
        validated_data.setdefault('author', self.context.get('author'))
        return Post.objects.create(**validated_data)
