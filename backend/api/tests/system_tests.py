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


#SYSTEM TESTING SECTION
#CONDUCT TEST ID: SYT1
class AuthorisedUserTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')
        self.login_url = reverse('login')

    def test_register_and_login(self):
        #register the test user with certain details
        register_data = {
            "username": "johndoe",
            "email": "johndoe@gmail.com",
            "password": "PaSsWoRd123"
        }
        response = self.client.post(self.register_url, register_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('user', response.json())

        #login the user with the valid registered credentials
        login_data = {
            "username": "johndoe",
            "password": "PaSsWoRd123"
        }

        #verify the sessions data and the username
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('user', response.json())
        self.assertEqual(response.json()['user']['username'], 'johndoe')

#CONDUCT TEST ID: SYT2
class ValidImageSearchTest(TestCase):
    #set up clean testing environment
    def setUp(self):
        self.client = APIClient()
        #get api endpoint url
        self.search_clothing_url = reverse('search-clothing') 
        #get path for test image
        self.test_image_path = 'C:/Users/janek/OneDrive - National College of Ireland/Desktop/sequintop.jpg'

        #upload an clothing item with an image to trigger the ORB extraction piepline
        image_path = 'C:/Users/janek/OneDrive - National College of Ireland/Desktop/sequintop.jpg'

        with open(image_path, 'rb') as image_file:
            Clothing.objects.create(
                name='ZARA sequin knit top',
                category='Top',
                price=9.99,
                image=File(image_file, name=os.path.basename(image_path)),
                url='https://www.zara.com/ie/en/sequinned-knit-peplum-top-p02142033.html?v1=423802578'
            )
    #test to check the system correctly returns visually similar matches
    def test_image_search_get_top_matches(self):
        with open(self.test_image_path, 'rb') as img:
            response = self.client.post(
                self.search_clothing_url,
                {'image': SimpleUploadedFile('test.jpg', img.read(), content_type='image/jpeg')},
                format='multipart'
            )

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        self.assertLessEqual(len(response.json()), 5)
        #return the visual similarity and match counts
        if response.json():
            self.assertIn('visual_similarity', response.json()[0])
            self.assertIn('match_count', response.json()[0])

#CONDUCT TEST ID: SYT3
class WishlistTest(TestCase):
    #set up clean testing environment
    def setUp(self):
        self.client = APIClient()

        #create a new user
        self.user = UserProfile.objects.create(
            username="johndoe",
            email="johndoe@gmail.com",
            #hash the password for security
            password=make_password("PaSsWoRd123")
        )

        #create a new clothing item
        self.clothing = Clothing.objects.create(
            name='ZARA sequin knit top',
                category='Top',
                price=9.99,
                image=SimpleUploadedFile("test.jpg", b"fake-image-data", content_type="image/jpeg")
        )

        self.add_url = "/api/wishlist/add/"
        self.view_url = "/api/wishlist/"

    def test_add_view_wishlist(self):
        #add the new item to the wishlist
        add_response = self.client.post(self.add_url, {
            'user_id' : self.user.id,
            'item_id' : self.clothing.id
        }, format='json'
        )

        self.assertEqual(add_response.status_code, 200)
        self.assertEqual(add_response.data['status'], 'added')

        #view the wishlist
        view_response = self.client.get(f"{self.view_url}?user_id={self.user.id}")
        self.assertEqual(view_response.status_code, 200)
        self.assertEqual(len(view_response.data), 1)
        self.assertEqual(view_response.data[0]['id'], self.clothing.id)

# CONDUCT TEST ID: SYT4
class SearchByKeywordTest(TestCase):
    #set up clean testing environment
    def setUp(self):
        self.client = APIClient()

        #create multiple clothing items
        Clothing.objects.create(
            name='ZW COLLECTION OVERSIZE POCKET SHIRT ORANGE',
            category='Top',
            price=45.95,
            image=SimpleUploadedFile("test.jpg", b"fake-image-data", content_type="image/jpeg")
        )
        Clothing.objects.create(
            name='ZW COLLECTION FITTED SHIRT BLACK',
            category='Top',
            price=55.95,
            image=SimpleUploadedFile("test.jpg", b"fake-image-data", content_type="image/jpeg")
        )
        Clothing.objects.create(
            name='ZW COLLECTION OVERSIZE WAISTCOAT ORANGE',
            category='Top',
            price=25.00,
            image=SimpleUploadedFile("test.jpg", b"fake-image-data", content_type="image/jpeg")
        )
        #create a keyword search query 
        self.search_url = "/api/search-keyword/?q=ORANGE"

    def test_keyword_search(self):
        #send the keyword serach request
        response = self.client.get(self.search_url)
        self.assertEqual(response.status_code, 200)
        #determine at least 2 results are returned
        results = response.json()
        self.assertGreaterEqual(len(results), 2)
        #extract price and put in price ascending order
        prices = [item['price'] for item in results]
        self.assertEqual(prices, sorted(prices))

