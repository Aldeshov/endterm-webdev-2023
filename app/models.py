from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Post(models.Model):
    code = models.PositiveIntegerField(validators=[MinValueValidator(8), MaxValueValidator(8)], unique=True)
    title = models.CharField(max_length=100)
    text = models.TextField()
    dateOfCreation = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
