from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=75)
    body = models.TextField()
    slug = models.SlugField()
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images/', default='fallback.png', blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    likes = models.ManyToManyField(User, related_name='post_likes', blank=True)
    #dislikes = models.ManyToManyField(User, related_name='post_dislikes', blank=True)

    def total_likes(self):
        return self.likes.count()

    # def total_dislikes(self):
    #     return self.dislikes.count()

    def __str__(self):
        return self.title



