from django.shortcuts import render
from .models import Comment, CommentLike, Follow, Post, PostLike
from .serialaizers import (CommentCreateSerializer, CommentDetailSerializer,
                          CommentLikeCreateSerializer,CommentLikeListSerializer,
                          FollowCreateSerializer, FollowListSerializer,
                          PostCreateSerializer, PostDetailSerializer,
                          PostLikeCreateSerializer, PostLikeListSerializer,
                          PostListSerializer)
from rest_framework import generics

class FollowListView(generics.ListAPIView):
    serializer_class = FollowListSerializer

    def get_queryset(self):
        return Follow.objects.filter(follower=self.request.user.id)


class FollowCreateView(generics.CreateAPIView):
    queryset= Follow.objects.all()
    serializer_class = FollowCreateSerializer

    def perform_create (self, serializer):
        serializer.save(follower=self.request.user.id)


class FollowDeleteView(generics.DestroyAPIView):
    serializer_class = FollowCreateSerializer


    def get_queryset(self):
        return Follow.objects.filter(follower=self.request.user.id)


class PostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer


class PostCreateView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer

    def perform_create(self, serializer):
       serializer.save(user=self.request.user.id)


class PostDetailView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer

class PostUpdateView(generics.UpdateAPIView):
    serializer_class = PostCreateSerializer
    def get_queryset(self):
       return Post.objects.filter(user=self.request.user.id)


class PostDeleteView(generics.DestroyAPIView):
    serializer_class = PostCreateSerializer

    def get_queryset (self):
       return Post.objects.filter (user=self.request. user. id)

class PostLikeListView(generics.ListAPIView):
    queryset = PostLike.objects.filter(like=True)
    serializer_class = PostLikeListSerializer


class PostLikeCreateView(generics.CreateAPIView):
    queryset = PostLike. objects.all()
    serializer_class = PostLikeCreateSerializer
    def perform_create (self, serializer):
        serializer.save(user=self.request. user.id)

class PostLikeDeleteView(generics.DestroyAPIView):
    queryset = PostLike. objects.all()
    serializer_class = PostLikeCreateSerializer
    def get_queryset (self, serializer):
        return PostLike.objects.filter(user=self.request.user.id)


class CommentCreateView(generics.CreateAPIView):
    queryset= Comment.objects.all()
    serializer_class = CommentCreateSerializer


    def perform_create (self, serializer):
        serializer.save(user=self.request.user.id)


class CommentDetailView(generics.RetrieveAPIView):
    queryset= Comment.objects.all()
    serializer_class = CommentDetailSerializer


class CommentUpdateView(generics.UpdateAPIView):
    serializer_class = CommentCreateSerializer

    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user.id)


class CommentDeleteView(generics.DestroyAPIView):
    serializer_class = CommentCreateSerializer


    def get_queryset(self):
      return Comment.objects.filter(user=self.request.user.id)


class CommentLikeListView (generics. ListAPIView):
    queryset = CommentLike.objects.filter (like=True)
    serializer_class = CommentLikeListSerializer


class CommentLikeCreateView(generics.CreateAPIView):
    queryset = CommentLike.objects.all()
    serializer_class = CommentLikeCreateSerializer


    def perform_create(self, serializer):
        serializer.save(user=self.request.user.id)


class CommentLikeDeleteView(generics.DestroyAPIView):
    serializer_class = CommentLikeCreateSerializer
    def get_queryset (self):
       return CommentLike.objects.filter(user=self.request.user.id)