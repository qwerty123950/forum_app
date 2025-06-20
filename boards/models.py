from django.db import models
from django.contrib.auth.models import User
import hashlib

class Board(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)
    is_deleted = models.BooleanField(default=False)  

    def __str__(self):
        return f"{self.name}"


class Topic(models.Model):
    subject = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey(Board, related_name='topics', on_delete=models.CASCADE)
    starter = models.ForeignKey(User, related_name='topics', on_delete=models.CASCADE)
    vote_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.board} -> {self.subject}"


class Post(models.Model):
    message = models.TextField(max_length=4000)
    topic = models.ForeignKey(Topic, related_name='posts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.CASCADE)
    def __str__(self):   
        return f"{self.topic} -> {self.message}"

class LongString(models.Model):
    content = models.TextField(unique=True)
    unique_id = models.CharField(max_length=10, unique=True)

    def save(self, *args, **kwargs):
        if not self.unique_id:
            self.unique_id = hashlib.sha256(self.content.encode()).hexdigest()[:8]
        super().save(*args, **kwargs)
