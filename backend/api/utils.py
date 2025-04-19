#this class contains methods used by other files in tis directory
import cv2
import numpy as np
from PIL import Image
from io import BytesIO


#Method to pick out orb keypoints (DRY)
def orb_keypoint_detection(image_input, is_base64=False):
    try:
        if is_base64:
            image_bytes = base64.b64decode(image_input)
            img = Image.open(BytesIO(image_input)).convert('RGB')
            image_np = np.array(img)
        else:
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