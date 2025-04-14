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


class ClothingItem(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=100)
    image = models.CharField(max_length=500)  
    price = models.DecimalField(max_digits=10, decimal_places=2)
    link = models.CharField(max_length=500)

    def __str__(self):
        return self.name
