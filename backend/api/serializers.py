from rest_framework import serializers
from .models import Clothing

class ClothingSerializer(serializers.ModelSerializer):
    #image field should return absolute urls
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Clothing
        fields = '__all__'  
