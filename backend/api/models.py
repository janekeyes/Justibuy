#from django.core.files.base import ContentFile
from django.db import models
from .utils import orb_keypoint_detection

class UserProfile(models.Model):
    username = models.CharField(max_length=150, unique=True, db_index=True)
    email = models.EmailField(unique=True, db_index=True)
    password = models.CharField(max_length=255)

    class Meta:
        db_table = 'user_profiles'
        verbose_name = 'User Profile'

    def __str__(self):
        return self.username



# class Clothing(models.Model):
#     name = models.CharField(max_length=255, null=True, blank=True)
#     category = models.CharField(max_length=255, null=True, blank=True)
#     #description = models.CharField(max_length=255, null=True, blank=True)
#     #size = models.CharField(max_length=50, null=True, blank=True)
#     price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
#     image = models.ImageField(upload_to='clothing_images/', blank=True, null=True)
#     keypoint_value = models.BinaryField(null=True, blank=True)
#     url = models.URLField(max_length=255, blank=True, null=True)

#     def save(self, *args, **kwargs):
#         super().save(*args, **kwargs)

#         if self.image and not self.keypoint_value:
#             try:
#                 ##call method from utils
#                 #keypoints, descriptors = orb_keypoint_detection(self.image.path)
#                 with self.image.open('rb') as image_file:
#                     keypoints, descriptors = orb_keypoint_detection(image_file)
      
#                 if descriptors is not None:
#                     #desc_bytes = descriptors.tobytes()
#                     self.keypoint_value = descriptors.tobytes()
#                     #super().save(update_fields=['keypoint_value'])
#                     Clothing.objects.filter(pk=self.pk).update(keypoint_value=self.keypoint_value)

#             except Exception as e:
#                 print(f"Error processing ORB keypoints: {e}")
class Clothing(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    category = models.CharField(max_length=255, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='clothing_images/', blank=True, null=True)
    keypoint_value = models.BinaryField(null=True, blank=True)
    url = models.URLField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        first_save = not self.pk
        super().save(*args, **kwargs)  # Save image to disk

        if self.image and (first_save or not self.keypoint_value):
            try:
                keypoints, descriptors = orb_keypoint_detection(self.image.path)
                if descriptors is not None:
                    self.keypoint_value = descriptors.tobytes()
                    super().save(update_fields=['keypoint_value'])  # Second save with keypoints
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
