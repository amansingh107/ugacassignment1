from django.db import models
from django.contrib.auth.models import User

class Booklet(models.Model):
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='booklets/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
