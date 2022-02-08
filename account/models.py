from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image
from io import BytesIO
from django.core.files import File




class User(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, null=True)
    image = models.ImageField(upload_to='profile', default="user.png")

    def save(self, *args, **kwargs):
        if not self.image.closed:
            img = Image.open(self.image)
            img.thumbnail((500, 500), Image.ANTIALIAS)

            tmp = BytesIO()
            img.save(tmp, 'PNG')
            self.image = File(tmp, 'image.png')
        return super().save(*args, **kwargs)