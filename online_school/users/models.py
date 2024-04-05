from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    birth_date = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=15, unique=True)
    customuser_group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.email
    
class Profile(models.Model):
    user=models.OneToOneField(CustomUser, null=True, on_delete=models.CASCADE)
    bio=models.TextField(null=True, blank=True)
    #profile_pic = models.ImageField(null=True, blank=True, upload_to="images/profile/")
    
def __str__(self):
    return str(self.user)
