from rest_framework import serializers
from .models import Comment, CommentLike, Follow, Post, PostLike



class FollowListSerializer(serializers.ModelSerializer):
     class Meta:
         model = Follow
         fields = ("id", "following", "created_date")


class FollowCreateSerializer(serializers.ModelSerializer):
     class Meta:
         model = Follow
         fields = ("following",)


class PostListSerializer(serializers.ModelSerializer):
    count_like = serializers.SerializerMethodField()
    count_comment = serializers.SerializerMethodField()
    class Meta:
       model = Post
       fields =("id", "user", "content", "count_like", "count_comment", 'created_date')


    def get_count_like (self, obj):
        return obj.likes.filter(like= True).count()

    def get_count_comment (self, obj):
        return obj.comments.count()


class PostDetailSerializer(serializers.ModelSerializer):
    count_like = serializers.SerializerMethodField()
    count_comment = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ("id", "user", "content", "description",
                  "count_like", "count_comment", 'created_date')

    def get_count_like(self, obj):
        return obj.likes.filter(like=True).count()


    def get_count_comment(self, obj):
        return obj.comments.count()


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
       model = Post
       fields = ("content", "description")

class PostLikeListSerializer(serializers.ModelSerializer):
     class Meta:
        model = PostLike
        fields = ("id", "user")


class PostLikeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = ( "post", "like")


class CommentDetailSerializer(serializers.ModelSerializer):
    count_like_comment = serializers.SerializerMethodField()
    class Meta:
       model = Comment
       fields = ("id", "user", "post", "text", "created_date","count_like_comment")
    def get_count_like_comment(self, obj):
        return obj.likes.filter(like=True).count()


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
       model = Comment
       fields = ("id", "post", "text")


class CommentLikeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentLike
        fields = ("id", "user")


class CommentLikeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentLike
        fields = ("comment", "like")