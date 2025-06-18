from rest_framework import serializers
from .models import Board, Topic, Post
from django.contrib.auth.models import User
from django.urls import reverse


class BoardSerializer(serializers.ModelSerializer):
    topics_url=serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = ['id', 'name', 'description', 'topics_url']

    def get_topics_url(self, obj):
        request=self.context.get('request')
        url = reverse('board-topics', kwargs={'board_id': obj.id})
        return request.build_absolute_uri(url) if request else url


class TopicSerializer(serializers.ModelSerializer):
    posts_url=serializers.SerializerMethodField()

    class Meta:
        model = Topic
        fields = ['id', 'subject', 'last_updated', 'board', 'starter', 'vote_count', 'posts_url']

    def get_posts_url(self, obj):
        request=self.context.get('request')
        url=reverse('topic-posts',kwargs={'topic_id': obj.id})
        return request.build_absolute_uri(url)


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'message', 'topic', 'created_at', 'updated_at', 'created_by', 'updated_by']
        read_only_fields = ['created_by', 'updated_by']

