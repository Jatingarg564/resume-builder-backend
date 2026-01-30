from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Custom user model.
    Right now it is same as Django user,
    but future-proof for companies.
    """
    pass

