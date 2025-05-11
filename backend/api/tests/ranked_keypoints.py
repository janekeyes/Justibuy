import cv2
import numpy as np
import os

def detect_orb(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError(f"Could not load image: {image_path}")
    orb = cv2.ORB_create(nfeatures=1000)
    keypoints, descriptors = orb.detectAndCompute(image, None)
    return image, keypoints, descriptors

def draw_match_image(test_img, test_kp, comp_img, comp_kp, matches, match_count_text):
    match_vis = cv2.drawMatches(test_img, test_kp, comp_img, comp_kp, matches[:20], None,
                                flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

    #match count text
    cv2.putText(match_vis, match_count_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 255, 0), 2, cv2.LINE_AA)
    return match_vis

#paths
test_image_path = r"backend\media\clothing_images\test-image.jpg"
comparison_paths = [
    r"backend\media\clothing_images\test-image.jpg",
    r"backend\media\clothing_images\comp2.jpg",
    r"backend\media\clothing_images\comp3.jpg"
]

#detect keypoints/descriptors in test image
test_img, test_kp, test_des = detect_orb(test_image_path)
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

#store comparison visuals
match_visuals = []

for i, comp_path in enumerate(comparison_paths):
    comp_img, comp_kp, comp_des = detect_orb(comp_path)
    matches = bf.match(test_des, comp_des)
    matches = sorted(matches, key=lambda x: x.distance)
    
    match_count_text = f"Matches: {len(matches)}"
    vis = draw_match_image(test_img, test_kp, comp_img, comp_kp, matches, match_count_text)
    match_visuals.append(vis)

#resize 
heights = [img.shape[0] for img in match_visuals]
min_height = min(heights)
resized_visuals = [cv2.resize(img, (int(img.shape[1] * min_height / img.shape[0]), min_height)) for img in match_visuals]

#stack visuals 
final_collage = cv2.hconcat(resized_visuals)

#save image
output_path = r"backend\media\demo_images\comparison_collage.jpg"
cv2.imwrite(output_path, final_collage)
print(f"Saved comparison collage to {output_path}")
