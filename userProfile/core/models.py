from django.db import models
from django.contrib.auth.models import User 
# Create your models here.


class userProfile (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    height = models.FloatField(null=True)
    weight = models.FloatField(null=True)
    age = models.IntegerField(null=True)
    sex = models.CharField(max_length=10, null=True)
    lifestyle = models.CharField(max_length=20, null=True)
    tags = models.TextField(max_length=200, null=True)
    diet = models.CharField(max_length=20, null=True)
    disease = models.CharField(max_length=100, null = True)
    allergy = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.user.username
    
