from django.test import TestCase
from api.utils import orb_keypoint_detection, descriptors_from_bytes, top_matches
from collections import namedtuple
from api.views import return_matches
from api.serializers import ClothingSerializer
from api.models import Clothing
import os
import numpy as np
import cv2

#CONDUCT UNT1
class TestORBDetection(TestCase):
    def test_orb_keypoint_detection(self):
        #path to test image
        image_path = os.path.join('api', 'tests', 'test_data', 'dress2.jpg')
        # Ensure file exists before running test
        self.assertTrue(os.path.exists(image_path), f"Test image not found at {image_path}")
        #run the keypoint descriptor function
        keypoints, descriptors = orb_keypoint_detection(image_path)
        #verify the descriptors were returned
        self.assertIsNotNone(descriptors, " ORB Descriptos for image.")
        self.assertGreater(len(descriptors), 0, "Descriptors shoudln't be empty.")

#CONDUCT UNT2
class ConvertDescriptorsTest(TestCase):
    def test_descriptors_from_bytes_valid_conversion(self):
    
        #create a orb descriptor array for testing purpose
        original = np.random.randint(0, 256, (5, 32), dtype=np.uint8)
        byte_data = original.tobytes()

        #use the existing function to convert the Byte array back to a NumPy array
        reconstructed = descriptors_from_bytes(byte_data)

        #ensure the returned value is a numpy array
        self.assertIsInstance(reconstructed, np.ndarray)
        #ensure the value is the same format as it was created
        self.assertEqual(reconstructed.shape, (5, 32))
        self.assertTrue(np.array_equal(original, reconstructed))

#CONDUCT UNT3
#create a clothing item with a price
TestItem = namedtuple('TestItem', ['price'])
class TopMatchTest(TestCase):
    def test_top_matches(self):
        #populate the test database with items
        #the prices should differ, and there should be a different average distances for each item
        matches = [
            (TestItem(price=10.99), 20),
            (TestItem(price=9.99), 20),
            (TestItem(price=19.99), 40),
            (TestItem(price=16.99), 50),
            (TestItem(price=17.99), 30),
            (TestItem(price=20.99), 80),
        ]
        top = top_matches(matches, k=5)

        #determine the expected order of items based on matches and then price
        expected_order = [
            (TestItem(price=9.99), 20),
            (TestItem(price=10.99), 20),
            (TestItem(price=17.99), 30),
            (TestItem(price=19.99), 40),
            (TestItem(price=16.99), 50),
        ]
        #assertain that the actual result order matches the expected order
        self.assertEqual(top, expected_order)


#CONDUCT UNT4
class ReturnMatchesTest(TestCase):
    def setUp(self):
        #create keypoint descriptors for test
        self.descriptors = np.random.randint(0, 256, (10, 32), dtype=np.uint8)
        #create clothing item, with descriptores stored as bytes
        self.clothing_item = Clothing.objects.create(
            name="Pink Dress",
            category="Dress",
            price=45.95,
            keypoint_value=self.descriptors.tobytes()
        )
        self.user_descriptors = np.random.randint(0, 256, (10, 32), dtype=np.uint8)
        self.bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        #generate the average distnace for test
        self.best_matches = [(self.clothing_item, 30.0)] 
    #create the test
    def test_return_matches(self):
        result = return_matches(self.best_matches, self.user_descriptors, self.bf)

        self.assertEqual(len(result), 1)
        item_data = result[0]

        # check the expected fields
        self.assertIn('name', item_data)
        self.assertIn('visual_similarity', item_data)
        self.assertIn('match_count', item_data)
        #check the values
        self.assertIsInstance(item_data['visual_similarity'], str)
        self.assertTrue(item_data['visual_similarity'].endswith('%'))
        self.assertIsInstance(item_data['match_count'], int)