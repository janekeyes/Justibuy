from django.db import models

from django.db import models

class UserProfile(models.Model):
    username = models.CharField(max_length=150, unique=True, db_index=True)
    email = models.EmailField(unique=True, db_index=True)
    password = models.CharField(max_length=255)  # Stores hashed passwords

    class Meta:
        db_table = 'user_profiles'  # Custom table name
        verbose_name = 'User Profile'

    def __str__(self):
        return self.username


class ClothingItem(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    size = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='clothing_images/')  # Ensure MEDIA settings in Django

    def __str__(self):
        return self.name
