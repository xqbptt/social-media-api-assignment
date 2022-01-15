from rest_framework import serializers
from .models import Post,Comment

class PostSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    class Meta:
        model = Post
        fields = ['id','title','desc','created_at']

class CommentSerializer(serializers.ModelSerializer):
    content = serializers.CharField(write_only=True)
    class Meta:
        model = Comment
        fields = ['id','content']

class PostListSerializer(serializers.ModelSerializer):
    comments = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='content',
     )
    likes = serializers.IntegerField(
    source='likes.count', 
    read_only=True
    )
    class Meta:
        model = Post
        fields = ['id','title','desc','created_at','comments','likes']