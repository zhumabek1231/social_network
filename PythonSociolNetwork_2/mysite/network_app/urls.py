from django.urls import path
from .views import (CommentCreateView,CommentDeleteView,CommentDetailView,
                    CommentLikeCreateView,CommentLikeDeleteView,CommentLikeListView,
                    CommentUpdateView,FollowCreateView,FollowDeleteView,
                    FollowListView,PostCreateView,PostDeleteView,PostDetailView,
                    PostLikeCreateView,PostLikeListView,
                    PostListView,PostUpdateView,PostLikeDeleteView)
urlpatterns =[
    path("follows/", FollowListView.as_view(), name="follow-list"),
    path("follows/create/", FollowCreateView.as_view(), name="follow-create"),
    path("follows/<int:pk>/delete/", FollowDeleteView.as_view(), name="follow-delete"),

    path("posts/", PostListView.as_view(), name="post-list"),
    path("posts/create/", PostCreateView.as_view(), name="post-create"),
    path("posts/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("posts/<int:pk>/update/", PostUpdateView.as_view(), name="post-update"),
    path("posts/<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"),

    path("post_likes/", PostLikeListView.as_view(), name="post-like-list"),
    path("post_likes/create/",PostLikeCreateView.as_view, name="post-like-create"),
    path("post_likes/<int:pk>/delete/", PostLikeDeleteView.as_view(), name="post-like-delete"),

    path("comments/create/", CommentCreateView.as_view(), name="comment-create"),
    path("comments/<int:pk>/", CommentDetailView.as_view(), name="comment-detail"),
    path("comments/<int:pk>/update/", CommentUpdateView.as_view(), name="comment-update"),
    path("comments/<int:pk>/delete/", CommentDeleteView. as_view(), name="comment-delete"),

    path("comment_likes/", CommentLikeListView.as_view(), name="comment-like-list"),
    path("comment_likes/create/", CommentLikeCreateView. as_view(), name="comment-like-create"),
    path("comment_likes/<int:pk>/delete/", CommentLikeDeleteView. as_view(), name="comment-like-delete"),
]