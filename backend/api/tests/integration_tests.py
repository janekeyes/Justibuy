from django.test import TestCase
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile
from api.models import Clothing
import tempfile
import cv2
import numpy as np
import os
from api.utils import orb_keypoint_detection
from django.conf import settings
from django.urls import reverse


# CONDUCT TEST: INT1
class ClothingSearchViewTest(TestCase):
    #set up clean testing environment
    def setUp(self):
        self.client = APIClient()
        #load the test image
        image_path = os.path.join(settings.BASE_DIR, 'api', 'tests', 'test_data', 'dress2.jpg')
        #extract ORB descriptors
        _, descriptors = orb_keypoint_detection(image_path)
        #create clothing item for the test image
        self.item = Clothing.objects.create(
            name='Pink Dress',
            category='Dress',
            price=19.99,
            keypoint_value=descriptors.tobytes()
        )
        self.upload_img_path = image_path
    #run the test
    def test_image_search_returns_matches(self):
        #open the test image file
        with open(self.upload_img_path, 'rb') as img:
            #send the request to the image search API, how image searching would work
            response = self.client.post('/api/search-clothing/', {
                'image': SimpleUploadedFile('test.jpg', img.read(), content_type='image/jpeg')
            })
        #test to check for success code
        self.assertEqual(response.status_code, 200)
        #test to check for minumum 1 sucessful match
        self.assertTrue(len(response.data) > 0)
        #return response with similarity annd number of matches, and item name
        self.assertIn('visual_similarity', response.data[0])
        self.assertIn('match_count', response.data[0])
        self.assertEqual(response.data[0]['name'], 'Pink Dress')

# CONDUCT TEST: INT2
class KeywordSearchTest(TestCase):
    #set up clean testing environment
    def setUp(self):
        self.client = APIClient()
        #create clothing items to populate the test database, two conatining th keyword
        Clothing.objects.create(name="Pink Dress", category="Dress", price=35.95, url="http://fake/url.com")
        Clothing.objects.create(name="Pink Shirt", category="Top", price=25.50, url="http://fake/url.com")
        Clothing.objects.create(name="Blue Skirt", category="Bottoms", price=40.50, url="http://fake/url.com")

    def test_keyword_search_sorted_by_price(self):
        #send get request to the keyword search endpoint with the query
        response = self.client.get('/api/search-keyword/?q=pink')
        self.assertEqual(response.status_code, 200)

        #extract the prices from the response
        prices = [item['price'] for item in response.json()]
        #ensure items are returned in price ascending order
        self.assertEqual(prices, sorted(prices))

        #check that only pink related items are returned
        names = [item['name'].lower() for item in response.json()]
        for name in names:
            self.assertIn('pink', name)


# CONDUCT TEST: INT2
class ClothingUploadTest(TestCase):
     #set up clean testing environment
    def setUp(self):
        self.client = APIClient()

    def test_image_upload_triggers_keypoint_extraction(self):
        #open and upload the test image
        with open("api/tests/test_data/dress2.jpg", "rb") as image_file:
            image_data = SimpleUploadedFile("dress2.jpg", image_file.read(), content_type="image/jpeg")
        #create the new item in the test database
        data = {
            "name": "Pink Dress",
            "category": "Dress",
            "price": 34.95,
            "image": image_data
        }
        #send the request to the clothing endpoint, creating the model and triggering the ORB extraction pipeline
        url = reverse("clothing-list")
        response = self.client.post(url, data=data, format="multipart")
        if response.status_code != 201:
            print("Response content:", response.content.decode())
        self.assertEqual(response.status_code, 201)

        #find newly created item from test database to verify it has been saved
        item = Clothing.objects.get(name="Pink Dress")
        #verify the keypoint was written and is not empty
        self.assertIsNotNone(item.keypoint_value)
        self.assertTrue(len(item.keypoint_value) > 0)
