from django.urls import path
from .views import *
from Authentication.views import LoginAPIView
urlpatterns = [
    path('authenticate',LoginAPIView.as_view(),name='authenticate'),
    path('follow/<int:pk>', FollowView.as_view(), name="follow-user"),
    path('unfollow/<int:pk>', UnfollowView.as_view(), name="unfollow-user"),
    path('user', UserView.as_view(), name="user-detail"),
    path('posts/',PostCreateView.as_view(), name="post-create"),
    path('posts/<int:pk>', PostDetailView.as_view(), name="post-get-delete"),
    path('like/<int:pk>', LikeView.as_view(), name="like-post"),
    path('unlike/<int:pk>', UnlikeView.as_view(), name="unlike-post"),
    path('comment/<int:pk>', CommentCreateView.as_view(), name="comment-create"),
    path('all_posts',PostListView.as_view(),name='post-list'),
]
