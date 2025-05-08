from rest_framework import serializers
from .models import Clothing, Wishlist


#data need to be converted to JSON and back to be used for API requests/responses

#SERIALIZE CLOTHING DATA
class ClothingSerializer(serializers.ModelSerializer):
    #return the full url for the image to ensure the image can be seen on the frontend
    image = serializers.ImageField(use_url=True)

    class Meta:
        #use the clothing model and all of its fields
        model = Clothing
        fields = '__all__'  
        
#SERIALIZE WISHLIST DATA        
class WishlistSerializer(serializers.ModelSerializer):
    
    class Meta:
        #use the wishlist model and all of its fields
        model = Wishlist
        fields = '__all__'