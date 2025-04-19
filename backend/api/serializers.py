from rest_framework import serializers
from .models import Clothing

class ClothingSerializer(serializers.ModelSerializer):
    #image field should return absolute urls
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Clothing
        fields = '__all__'  
        #field sthat are not images should be marked as optional, to allow for user image upload
        extra_kwargs = {
            'name': {'required': False},
            'category': {'required': False},
            'description': {'required': False},
            'size': {'required': False},
            'price': {'required': False},
        }
