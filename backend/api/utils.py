#------REFERENCES-------
# https://docs.opencv.org/3.4/d1/d89/tutorial_py_orb.html
# https://www.geeksforgeeks.org/feature-matching-using-orb-algorithm-in-python-opencv/
# https://docs.opencv.org/4.x/dc/dc3/tutorial_py_matcher.html
# https://www.geeksforgeeks.org/python-opencv-bfmatcher-function/
# https://stackoverflow.com/questions/20145842/python-sorting-by-multiple-criteria


# This class contains methods used by other files in this directory
import cv2
import numpy as np
from PIL import Image
import io

def user_credentials(data, required_fields):
    error = {}
    for field in required_fields:
        if not data.get(field):
            error[field] = f'{field} is a required field'
    return error


#Method to pre process the image
def preprocess(image_path, target_size):
    #ref: https://www.geeksforgeeks.org/load-images-in-tensorflow-python/
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Image could not be loaded.")

    # 1. Resize while keeping aspect ratio
    # ref: https://pytutorial.com/python-resize-image-while-keeping-aspect-ratio/
    # ref: https://codoraven.com/tutorials/opencv-vs-pillow/resize-image-keep-aspect-ratio/
    height, width = image.shape[:2]
    scope = target_size / max(height, width)
    width_new = int(width * scope)
    height_new = int(height * scope) 
    resized = cv2.resize(image, (width_new , height_new), interpolation=cv2.INTER_AREA)
    #determine how much padding is needed to reach a square shape
    width_padding= target_size - width_new
    height_padding = target_size - height_new
    #calculate each sides padding
    top, bottom = height_padding // 2,
    height_padding - (height_padding // 2)
    left, right = width_padding // 2, 
    width_padding - (width_padding // 2)
    #add the padding using opencv
    # ref: https://docs.opencv.org/4.x/dc/da3/tutorial_copyMakeBorder.html
    square_image = cv2.copyMakeBorder(resized, top, bottom, left, right, cv2.BORDER_CONSTANT, value=[0, 0, 0])
    gray = cv2.cvtColor(square_image, cv2.COLOR_BGR2GRAY)

    #higher the image contrast for better feature keypoint feature detection
    # ref: https://www.geeksforgeeks.org/clahe-histogram-eqalization-opencv/
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))#default size
    processed = clahe.apply(gray)

    return processed


#mthod to pick out ORB keypoints 
#keypoints are detected in the image and the ORB descriptors are calculated which are then saved as binary in the keypoint value field
def orb_keypoint_detection(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError("Failed to load image for ORB detection.")

    orb = cv2.ORB_create(nfeatures=1000)
    keypoints, descriptors = orb.detectAndCompute(image, None)

    if descriptors is None:
        raise ValueError("No descriptors found in image.")

    return keypoints, descriptors

# Method to compare the uploaded user image to database images
def compare_keypoints(descriptors_query, clothing_query):
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    results = []

    for clothing in clothing_query:
        if clothing.keypoint_value:
            try:
                # Ensure correct shape
                descriptors_db = descriptors_from_bytes(clothing.keypoint_value)
                matches = bf.match(descriptors_query, descriptors_db)
                matches = sorted(matches, key=lambda x: x.distance)

                distance = sum(match.distance for match in matches)
                average_distance = distance / len(matches) if matches else float('inf')

                results.append({
                    'clothing': clothing,
                    'number_of_matches': len(matches),
                    'average_distance': average_distance,
                })

            except Exception as e:
                print(f"Error. Could not match {clothing.id}: {e}")

    #return the best results first
    return sorted(results, key=lambda x: x['average_distance'])


#function to rebuild the orb descriptor from stored item blob of bytes
def descriptors_from_bytes(byte_data):
    return np.frombuffer(byte_data, dtype=np.uint8).reshape(-1, 32)

#function to filter visual matches, getting the average distance
def match_by_disance(user_descriptors, clothing_query, bf, threshold=70):
    matches_per_item = []

    for item in clothing_query:
        try:
            db_descriptors = descriptors_from_bytes(item.keypoint_value)
            matches = bf.match(user_descriptors, db_descriptors)
            if matches:
                avg_distance = sum(m.distance for m in matches) / len(matches)
                if avg_distance < threshold:
                    matches_per_item.append((item, avg_distance))
        except Exception as e:
            print(f"Matching error for item {item.id}: {e}")
            continue

    return matches_per_item

#get good matches
def get_good_matches(user_descriptors, clothing_query, bf, threshold=70):
    matches_per_item = []

    for item in clothing_query:
        try:
            db_descriptors = descriptors_from_bytes(item.keypoint_value)

            matches = bf.match(user_descriptors, db_descriptors)
            if matches:
                # Get the average distance between matches
                # The lower the distance, the better the match
                average_distance = sum(m.distance for m in matches) / len(matches)
                #filter out all the bad matches
                if average_distance < 70:
                    matches_per_item.append((item, average_distance))
        except Exception as e:
            print(f"Matching error for item {item.id}: {e}")
            continue

    return matches_per_item

#sort the matches by visual similarity and then by lowest price
def top_matches(item_matches, k=5):
    sorted_matches = sorted(item_matches, key=lambda x: (x[1], x[0].price or 0))
    return sorted_matches[:k]
