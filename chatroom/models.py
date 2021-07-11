from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """ Change the representation of the default User model
    """

    def __str__(self):
        return f"{self.id}.  {self.username} ({self.email}):  {self.first_name} {self.last_name}"


class Message(models.Model):
    """Model for data persistence of messages sent in a chatroom
    """

    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name="messages")

    room_name = models.CharField(max_length=255)
    message = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)

    # Order messages by their timestamps
    class Meta:
        ordering = ('creation_date',)
