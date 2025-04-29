# This class contains methods used by other files in this directory
import cv2
import numpy as np
from PIL import Image
import io


# Method to pick out ORB keypoints (DRY)
# def orb_keypoint_detection(image_input):
#     try:
#         # Read image from file-like object (InMemoryUploadedFile)
#         image_bytes = image_input.read()
#         image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
#         image_np = np.array(image)

#         # Convert to grayscale
#         gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)

#         orb = cv2.ORB_create()
#         keypoints = orb.detect(gray, None)

#         #compute descriptors id keypoints are detected
#         if keypoints:
#             keypoints, descriptors = orb.compute(gray, keypoints)

#             #check if the descriptors are none
#             if descriptors is None:
#                 raise ValueError("No descriptors found")

#         return keypoints, descriptors
#     except Exception as e:
#         raise ValueError(f"Detection failure: {str(e)}")

#keypoints are detected in the image and the ORB descriptors are calculated which are then saved as binary in the keypoint value field
def orb_keypoint_detection(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError("Failed to load image for ORB detection.")

    orb = cv2.ORB_create()
    keypoints, descriptors = orb.detectAndCompute(image, None)

    if descriptors is None:
        raise ValueError("No descriptors found in image.")

    return keypoints, descriptors

# Method to compare the uploaded user image to database images
def compare_keypoints(descriptors_query, clothing_queryset):
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    results = []

    for clothing in clothing_queryset:
        if clothing.keypoint_value:
            descriptors_db = np.frombuffer(clothing.keypoint_value, dtype=np.uint8)
            try:
                # Ensure correct shape
                descriptors_db = descriptors_db.reshape(-1, 32)
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

    # Return the best results first
    return sorted(results, key=lambda x: x['average_distance'])
