from os import stat
import queue
from django.shortcuts import render
from rest_framework import generics,status,permissions
from rest_framework.views import APIView
from Authentication.models import User
from rest_framework.response import Response
from .serializers import PostSerializer, CommentSerializer, PostListSerializer
from .models import Post,Comment
from .permissions import IsOwner
# Create your views here.


class FollowView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request, pk, format=None):
        current_user = self.request.user

        try:
            target_user = User.objects.get(id=pk)
        except:
            return Response({"This user does not exist"},status.HTTP_404_NOT_FOUND)

        if current_user in target_user.followers.all():
            return Response({"Already following"},status.HTTP_400_BAD_REQUEST)

        target_user.followers.add(current_user.id)
        current_user.following.add(target_user.id)

        return Response({"Followed Successfully"},status.HTTP_200_OK)

class UnfollowView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request, pk, format=None):
        current_user = self.request.user

        try:
            target_user = User.objects.get(id=pk)
        except:
            return Response({"This user does not exist"},status.HTTP_404_NOT_FOUND)

        if current_user not in target_user.followers.all():
            return Response({"Not following this user"},status.HTTP_400_BAD_REQUEST)

        target_user.followers.remove(current_user.id)
        current_user.following.remove(target_user.id)

        return Response({"Unfollowed Successfully"},status.HTTP_200_OK)

class UserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request, format=None):
        current_user = self.request.user
        user_data = {
            'username':current_user.username,
            'num_followers':current_user.followers.count(),
            'num_followings':current_user.following.count(),
        }
        return Response(user_data,status.HTTP_200_OK)

class PostCreateView(generics.CreateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def post(self):
        serializer = PostSerializer(data = self.request.data)
        if serializer.is_valid():
            serializer.save(user = self.request.user)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    queryset = Post.objects.all()
    lookup_field = 'pk'

    def get(self,request, pk, format=None):
        post = Post.objects.get(id=pk)
        post_data = {
            'id': post.id, 
            'num_likes': post.likes.count(),
            'comments': post.comments.count(),
        }
        return Response(post_data,status=status.HTTP_200_OK)

class LikeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request, pk, format=None):
        current_user = self.request.user

        try:
            post = Post.objects.get(id=pk)
        except:
            return Response({"This post does not exist"},status.HTTP_404_NOT_FOUND)

        if current_user in post.likes.all():
            return Response({"Already liked"},status.HTTP_400_BAD_REQUEST)

        post.likes.add(current_user.id)
        return Response({"Liked Successfully"},status.HTTP_200_OK)

class UnlikeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request, pk, format=None):
        current_user = self.request.user

        try:
            post = Post.objects.get(id=pk)
        except:
            return Response({"This post does not exist"},status.HTTP_404_NOT_FOUND)

        if current_user not in post.likes.all():
            return Response({"Not liked this post"},status.HTTP_400_BAD_REQUEST)
            
        post.likes.remove(current_user.id)
        return Response({"Unliked Successfully"},status.HTTP_200_OK)

class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request, pk, format=None):
        serializer = CommentSerializer(data = self.request.data)
        try:
            post = Post.objects.get(id=pk)
        except:
            return Response({"This post does not exist"},status.HTTP_404_NOT_FOUND)
        if serializer.is_valid():
            comment = serializer.save(user = self.request.user)
            post.comments.add(comment.id)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    serializer_class = PostListSerializer
    def get_queryset(self):
        return Post.objects.all().filter(user=self.request.user).order_by('created_at')