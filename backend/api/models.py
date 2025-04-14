from django.db import models

class UserProfile(models.Model):
    username = models.CharField(max_length=150, unique=True, db_index=True)
    email = models.EmailField(unique=True, db_index=True)
    password = models.CharField(max_length=255) 

    class Meta:
        db_table = 'user_profiles' 
        verbose_name = 'User Profile'

    def __str__(self):
        return self.username



class Clothing(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    size = models.CharField(max_length=50, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='clothing_images/', blank=True, null=True)  # Ensure upload path is correct

    def __str__(self):
        return self.name
