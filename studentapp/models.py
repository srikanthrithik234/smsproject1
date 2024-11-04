from django.db import models

class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    rating = models.IntegerField()  # You can use IntegerField for stars (1-5)
    issues = models.CharField(max_length=100)

    def __str__(self):
        return f"Feedback from {self.name}"
