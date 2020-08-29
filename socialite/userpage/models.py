from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    caption = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True, auto_now=False)
    image = models.ImageField(upload_to='userpage/images/')

    def __str__(self):
        # return str(self.user)+ "   :   " + str(self.date)
        return str(self.caption)

    @property
    def get_image(self):
        return self.image.url

    @property
    def like_count(self):
        return self.post.likes

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    userimage = models.ImageField(upload_to='user_img/profile/', null=True)
    bio = models.CharField(max_length=100, null=True)
    connection = models.CharField(max_length=1500, null=True)
    follower = models.IntegerField(default=0)
    following = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user)


class Like(models.Model):
    user = models.ManyToManyField(User, related_name='liking_user')
    post = models.OneToOneField(Post, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return str(self.post.caption)


class Following(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    followedby = models.ManyToManyField(User, related_name='followedby')
    followcount = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user.username)