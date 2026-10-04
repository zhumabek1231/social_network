from django.db import models

class Follow (models.Model):
   follower = models.PositiveIntegerField()
   following = models.PositiveIntegerField()
   created_date = models.DateTimeField(auto_now_add=True)

   def __str__(self):
     return f"{self. follower}, {self. following}"



class Post(models.Model):
   user = models.PositiveIntegerField()
   content = models.FileField(upload_to='posts/')
   description = models.TextField (null=True, blank=True)
   created_date = models.DateTimeField(auto_now_add=True)

   def __str__(self):
      return f"{self. content}, {self.user}"


class PostLike(models.Model):
   user = models.PositiveIntegerField()
   post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
   like = models. BooleanField(default=True)



class Comment(models.Model):
    user = models.PositiveIntegerField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name="comments")
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add = True)


class CommentLike(models.Model):
    user=models.PositiveIntegerField()
    comment = models.ForeignKey(Comment, on_delete=models. CASCADE, related_name="likes")
    like = models.BooleanField(default=True)

    def __str__(self):
        return f"{self. user}, {self.comment}, {self.like}"