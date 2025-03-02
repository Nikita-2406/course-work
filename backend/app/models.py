from django.db import models

class Users(models.Model):
    name = models.CharField(max_length=100)
    login = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=128)
    admin = models.BooleanField(default=False)

    def __str__(self):
        return self.login

class Files(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)
    file_link = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file_name


class Session(models.Model):
    session_id = models.CharField(max_length=200)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    login = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=128)