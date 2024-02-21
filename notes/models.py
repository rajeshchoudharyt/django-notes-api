from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


# Register User
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    

# Create Note
class Note(models.Model):
    note_id = models.BigAutoField(primary_key=True)
    email = models.EmailField(max_length=50)
    title = models.TextField(max_length=255)
    content = models.TextField(max_length=255)
    date_created = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('email', 'title')


# Share Note
class ShareNote(models.Model):
    note_id = models.ForeignKey(Note, on_delete=models.CASCADE)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('note_id', 'user_id')


# Edit Note
class EditNote(models.Model):
    note_id = models.ForeignKey(Note, on_delete=models.CASCADE)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now)
    content = models.TextField(max_length=255)

