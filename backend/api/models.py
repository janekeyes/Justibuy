import cv2
import numpy as np
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
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
    image = models.ImageField(upload_to='clothing_images/', blank=True, null=True)
    keypoint_value = models.BinaryField(null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image and not self.keypoint_value:
            img_path = self.image.path
            img_cv = cv2.imread(img_path)
            gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
            orb = cv2.ORB_create()
            keypoints = orb.detect(gray, None)
            keypoints, descriptors = orb.compute(gray, keypoints)

            if descriptors is not None:
                desc_bytes = descriptors.tobytes()
                self.keypoint_value = desc_bytes
                super().save(update_fields=['keypoint_value'])

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
