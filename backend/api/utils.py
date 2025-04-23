#this class contains methods used by other files in tis directory
import cv2
import numpy as np
# from PIL import Image
# from io import BytesIO


#Method to pick out orb keypoints (DRY)
def orb_keypoint_detection(image_input, is_base64=False):
    try:
        image_np = cv2.imread(image_input)
        if image_np is None:
            raise ValueError("Image not found")
        
        gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)

        orb = cv2.ORB_create()
        keypoints = orb.detect(gray, None)
        keypoints, descriptors = orb.compute(gray, keypoints)

        return keypoints, descriptors
    except Exception as e:
        raise ValueError(f"Detection failure: {str(e)}")
    
#method to compare the uploaded user image to database images
def compare_keypoints(descriptors_query, clothing_queryset):
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    results = []

    for clothing in clothing_queryset:
        if clothing.keypoint_value:
            descriptors_db = np.frombuffer(clothing.keypoint_value, dtype=np.uint8)
            try:
                #ensure correct shape
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

    #resturn the best results first
    return sorted(results, key=lambda x: x['average_distance'])

