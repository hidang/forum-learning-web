from django.db import models
from django.contrib.auth.models import User


# python3 manage.py makemigrations  :Khởi tạo file migrations tại các module có models
# python3 manage.py migrate         :apply file migrations được tạo từ model vào database
# Create your models here.


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    tag = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    thumbnail = models.ImageField(upload_to='images/', blank=True, null=True)
    author = models.ForeignKey(
        User, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def snippetContent(self):
        return self.content[:50] + "..."


class Comment(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(
        User, default=None, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
