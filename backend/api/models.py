# --------REFERENCES---------
# https://docs.djangoproject.com/en/5.2/ref/models/fields/
# https://docs.djangoproject.com/en/5.2/topics/files/
# https://docs.djangoproject.com/en/5.2/ref/models/fields/#binaryfield
# https://docs.djangoproject.com/en/5.2/topics/db/models/

from django.db import models
from .utils import orb_keypoint_detection

#USER MODEL - This creates the table for Justibuy users
class UserProfile(models.Model):
    #create the user fields
    username = models.CharField(max_length=150, unique=True, db_index=True)
    email = models.EmailField(unique=True, db_index=True)
    password = models.CharField(max_length=255)

    class Meta:
        db_table = 'user_profiles'
        verbose_name = 'User Profile'

    def __str__(self):
        return self.username

#WISHLIST MODEL - This creates the table for Justibuy user wishlists
class Wishlist(models.Model):
    #create the wishlist fields
    user = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    item = models.ForeignKey('Clothing', on_delete=models.CASCADE)

    #ensure that there are no duplicated items in the wishlist
    class Meta:
        unique_together = ('user', 'item')  

    def __str__(self):
        return f"{self.user.username} - {self.item.name}"


#CLOTHING MODEL - This creates the table for Justify clothing items
class Clothing(models.Model):
    #generate clothing item fields
    name = models.CharField(max_length=255, null=True, blank=True)
    category = models.CharField(max_length=255, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='clothing_images/', blank=True, null=True)
    #keypoint_value - this stores the image keypoint descriptors as a binary, to be used later for feature matching
    keypoint_value = models.BinaryField(null=True, blank=True)
    url = models.URLField(max_length=255, blank=True, null=True)

    #method for extracting and storing ORB keypoint descriptors when a new item is added to the database
    #custom save method, allows extra logic to be added after an image has been uploaded
    def save(self, *args, **kwargs):
        #check if item is being saved/updated
        first_save = not self.pk
        #save item image to the disk before processing
        super().save(*args, **kwargs) 

        if self.image and (first_save or not self.keypoint_value):
            try:
                #generate the ORB keypoints, call method from utils.py
                keypoints, descriptors = orb_keypoint_detection(self.image.path)
                if descriptors is not None:
                    #generate the keypoints descriptors as binary data
                    self.keypoint_value = descriptors.tobytes()
                    #save with keypoint value
                    super().save(update_fields=['keypoint_value'])
            #catch errors
            except Exception as e:
                print(f"Error processing ORB keypoints: {e}")


#Previous iteration: save keypoint image
# if descriptors is not None:
#     img_with_kp = cv2.drawKeypoints(img_cv, keypoints, None, color=(0, 255, 0), flags=0)
#
#     # Encode the image to a memory buffer
#     is_success, buffer = cv2.imencode(".jpg", img_with_kp)
#     if is_success:
#         io_buf = BytesIO(buffer)
#         self.image_keypoints.save(
#             f'kp_{self.image.name}', 
#             ContentFile(io_buf.read()), 
#             save=False
#         )
#
#     super().save(update_fields=['image_keypoints'])
