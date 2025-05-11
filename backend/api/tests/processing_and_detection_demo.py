import cv2
import numpy as np
import os

def preprocess(image_path, target_size):
    #load image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Image at {image_path} could not be loaded.")
    
    #resize 
    height, width = image.shape[:2]
    scale = target_size / max(height, width)
    new_width = int(width * scale)
    new_height = int(height * scale)
    resized = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
    
    #add padding to make it square
    padding_top = (target_size - new_height) // 2
    padding_bottom = target_size - new_height - padding_top
    padding_left = (target_size - new_width) // 2
    padding_right = target_size - new_width - padding_left
    square_image = cv2.copyMakeBorder(resized, padding_top, padding_bottom, padding_left, padding_right, 
                                      cv2.BORDER_CONSTANT, value=[0, 0, 0])

    return square_image

def orb_keypoint_detection(image):
    #convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    #create ORB detector & compute keypoints/descriptors
    orb = cv2.ORB_create(nfeatures=1000)
    keypoints, descriptors = orb.detectAndCompute(gray, None)
    
    #draw keypoints
    keypoint_image = cv2.drawKeypoints(image, keypoints, None, color=(0, 255, 0), flags=0)

    return keypoints, descriptors, keypoint_image

def match_keypoints(descriptors1, descriptors2, image1, image2, keypoints1, keypoints2):
    #match descriptors
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(descriptors1, descriptors2)

    #sort matches by distance 
    matches = sorted(matches, key=lambda x: x.distance)

    #draw matches 
    match_image = cv2.drawMatches(image1, keypoints1, image2, keypoints2, matches[:20], None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

    return match_image

def save_images(test_image_path, comparison_image_path, target_size, save_dir):
    #preprocess images 
    test_image = preprocess(test_image_path, target_size)
    comparison_image = preprocess(comparison_image_path, target_size)

    #detect keypoints & descriptors for  images
    keypoints1, descriptors1, keypoint_image1 = orb_keypoint_detection(test_image)
    keypoints2, descriptors2, keypoint_image2 = orb_keypoint_detection(comparison_image)

    #save images with detected keypoints
    keypoint_image1_path = os.path.join(save_dir, "test_image_keypoints.jpg")
    keypoint_image2_path = os.path.join(save_dir, "comparison_image_keypoints.jpg")
    cv2.imwrite(keypoint_image1_path, keypoint_image1)
    cv2.imwrite(keypoint_image2_path, keypoint_image2)

    #match keypoints both images
    match_image = match_keypoints(descriptors1, descriptors2, test_image, comparison_image, keypoints1, keypoints2)

    #save the image with matches
    match_image_path = os.path.join(save_dir, "matched_keypoints.jpg")
    cv2.imwrite(match_image_path, match_image)

    return keypoint_image1_path, keypoint_image2_path, match_image_path


save_dir = r"backend\media\demo_images"
test_image_path = r"backend\media\clothing_images\test-image.jpg"
comparison_image_path = r"backend\media\clothing_images\comparison_image.jpg"
target_size = 256  # Size to resize the images to

#save image
keypoint_image1_path, keypoint_image2_path, match_image_path = save_images(test_image_path, comparison_image_path, target_size, save_dir)

#output  paths
print(f"Keypoints image for test image saved at: {keypoint_image1_path}")
print(f"Keypoints image for comparison image saved at: {keypoint_image2_path}")
print(f"Matched keypoints image saved at: {match_image_path}")
