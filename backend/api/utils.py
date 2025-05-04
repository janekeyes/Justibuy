# This class contains methods used by other files in this directory
import cv2
import numpy as np
from PIL import Image
import io


#mthod to pick out ORB keypoints 
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

# #serialize the matched data to be returned to the UI
# def return_matches(best_matches, user_descriptors, bf):
#     matched_data = []

#     for item, score in best_matches:
#         item_data = ClothingSerializer(item).data
#         #item_data['match_score'] = round(score, 2)
#         #return item similarity as a percentage for user
#         similarity = max(0, 100 - score)
#         item_data['visual_similarity'] = f"{round(similarity)}%"
#         #calculate the number of matches
#         db_descriptors = descriptors_from_bytes(item.keypoint_value)
#         matches = bf.match(user_descriptors, db_descriptors)
#         item_data['match_count'] = len(matches)
#         matched_data.append(item_data)
#     return matched_data

