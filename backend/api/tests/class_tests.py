from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from api.models import UserProfile, Clothing, Wishlist
from django.core.files.uploadedfile import File, SimpleUploadedFile
from django.contrib.auth.hashers import make_password, check_password
from api.serializers import ClothingSerializer
from unittest.mock import patch
from PIL import Image
import os
import json


#this section uses mock testing: https://medium.com/@faviannauu/mock-in-python-unit-testing-8f56f67613aa
#CONDUCT CLT1
class ClothingSerializerTest(TestCase):
    #set up clean testing environment
    def setUp(self):
        #start patch for orb keypoint
        self.orb_patcher = patch('api.utils.orb_keypoint_detection')
        mock_orb = self.orb_patcher.start()
        mock_orb.return_value = ([], None)

        #create clothing item
        self.clothing = Clothing.objects.create(
            name='ZARA sequin knit top',
            category='Top',
            price=9.99,
            image='clothing_images/test.jpg', 
            url='https://www.zara.com/ie/en/sequinned-knit-peplum-top-p02142033.html?v1=423802578',
        )

    def tearDown(self):
        #end patch after test
        self.orb_patcher.stop()
        
    #create the test
    def test_serializers_fields(self):
        serializer = ClothingSerializer(instance=self.clothing)
        data = serializer.data
        #define the fields that are expected
        expected_fields = {'id', 'name', 'category', 'price', 'image', 'url', 'keypoint_value'}
        #check that the fields are present
        self.assertEqual(set(data.keys()), expected_fields)

#CONDUCT TEST ID: CLT2
class UserAuthTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.login_url = reverse('login')

    def test_register_user_hashes_password(self):
        data = {
            "username": "johndoe",
            "email": "johndoe@gmail.com",
            "password": "PaSsWoRd123"
        }
        response = self.client.post(self.register_url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)

        user = UserProfile.objects.get(username="johndoe")
        self.assertNotEqual(user.password, "PaSsWoRd123")
        self.assertTrue(check_password("PaSsWoRd123", user.password))

    def test_login_user_valid_credentials(self):
        #create and save hashed password
        from django.contrib.auth.hashers import make_password
        user = UserProfile.objects.create(
            username="johndoe",
            email="johndoe@gmail.com",
            password=make_password("PaSsWoRd123")
        )

        login_data = {
            "username": "johndoe",
            "password": "PaSsWoRd123"
        }
        response = self.client.post(self.login_url, data=json.dumps(login_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Login successful', response.content.decode())