from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """ Change the representation of the default User model
    """
    
    def __str__(self):
        return f"{self.id}.  {self.username} ({self.email}):  {self.first_name} + {self.last_name}"

