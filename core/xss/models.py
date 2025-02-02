from django.db import models

from django.contrib.auth import get_user_model

# Create your models here.
user_model = get_user_model()


class Comment(models.Model):
    user = models.ForeignKey(user_model, on_delete=models.CASCADE, blank=False, null=False)
    message = models.TextField(blank=False, null=False)

    def __str__(self):
        return self.message