#------REFERENCES-------
# https://docs.python.org/3/library/tempfile.html
# https://docs.djangoproject.com/en/5.2/topics/db/models/
# https://docs.djangoproject.com/en/5.2/topics/db/queries/
# https://docs.djangoproject.com/en/5.2/topics/http/views/#handling-errors
# https://docs.djangoproject.com/en/5.2/ref/request-response/#jsonresponse-objects
# https://docs.djangoproject.com/en/5.2/topics/auth/passwords/#using-the-password-hashers
# https://docs.djangoproject.com/en/5.2/topics/http/file-uploads/
# https://www.django-rest-framework.org/api-guide/serializers/
# https://www.django-rest-framework.org/api-guide/responses/#response-objects
# https://www.django-rest-framework.org/api-guide/parsers/#multipartparser

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import Q
import json
from .models import UserProfile, Clothing, Wishlist
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ClothingSerializer
from .utils import user_credentials, orb_keypoint_detection, descriptors_from_bytes, get_good_matches, top_matches, resize_saved_image
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.generics import RetrieveAPIView
import numpy as np
import cv2
import tempfile

#IMAGE SEARCH VIEW
class ClothingSearchView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        user_image = request.FILES.get('image')

        if not isinstance(user_image, InMemoryUploadedFile):
            return Response({'error': 'No valid image provided'}, status=400)

        try:
            #save the uploaded image to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp:
                for chunk in user_image.chunks():
                    tmp.write(chunk)
                temp_path = tmp.name

            #extract descriptors from user upload
            _, user_descriptors = orb_keypoint_detection(temp_path)
            if user_descriptors is None:
                return Response({'error': 'Could not extract features from image'}, status=400)

            bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
            clothing_query = Clothing.objects.exclude(keypoint_value=None)

            matches_per_item = get_good_matches(user_descriptors, clothing_query, bf)
            if not matches_per_item:
                return Response({'message': 'Could not find a match. Please try another image.'}, status=200)

            best_matches = top_matches(matches_per_item)
            matched_data = return_matches(best_matches, user_descriptors, bf)

            return Response(matched_data, status=200)
        except Exception as e:
            return Response({'error': f'Image search failed: {str(e)}'}, status=500)

#METHOD:seralize the matched data to be returned to the UI
#could not stay in utils as it caused a circular import error
def return_matches(best_matches, user_descriptors, bf):
    matched_data = []

    for item, score in best_matches:
        item_data = ClothingSerializer(item).data
        #item_data['match_score'] = round(score, 2)
        #return item similarity as a percentage for user
        similarity = max(0, 100 - score)
        item_data['visual_similarity'] = f"{round(similarity)}%"
        #calculate the number of matches
        db_descriptors = descriptors_from_bytes(item.keypoint_value)
        matches = bf.match(user_descriptors, db_descriptors)
        item_data['match_count'] = len(matches)
        matched_data.append(item_data)
    return matched_data


#SEARCH BY KEYWORD VIEW
#https://docs.djangoproject.com/en/5.2/topics/db/queries/
@api_view(['GET'])
def keyword_search(request):
    keyword = request.GET.get('q', '').strip()

    if not keyword:
        return Response({'error': 'PLease enter a valid serach term.'}, status=400)
    try:
        #filtering on name cateorgy and price fields as string (case sensitive)
        items = Clothing.objects.filter(Q(name__icontains=keyword) | Q(category__icontains=keyword) | Q(category__icontains=keyword)).order_by('price')
        if not items.exists():
            return Response({'message': 'Your search has no matches. PLease try another term'}, status=200)
        serializer = ClothingSerializer(items, many=True)
        return Response(serializer.data, status=200)
    
    except Exception as e:
        return Response({'error': f'Keyword search failed: {str(e)}'}, status=500)

        
class ClothingDetailView(RetrieveAPIView):
    queryset = Clothing.objects.all()
    serializer_class = ClothingSerializer


# Register view with password hashing
@csrf_exempt
def RegisterUser(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            required_fields = ['username', 'email', 'password']
            
            # Validate the fields
            errors = user_credentials(data, required_fields)
            if errors:
                return JsonResponse({'error': errors}, status=400)

            username = data['username'].strip()
            email = data['email'].strip().lower()
            password = data['password']

            # Check if username or email already exists
            if UserProfile.objects.filter(username=username).exists():
                return JsonResponse({'error': 'Username already exists'}, status=400)
            if UserProfile.objects.filter(email=email).exists():
                return JsonResponse({'error': 'Email already exists'}, status=400)

            hashed_password = make_password(password)
            user = UserProfile(username=username, email=email, password=hashed_password)
            user.save()

            return JsonResponse({'message': 'User registered successfully', 'user': {'id': user.id, 'username': user.username}}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

#LOGIN VIEW
@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        required_fields = ['username', 'password']
        
        # Validate the fields
        errors = user_credentials(data, required_fields)
        if errors:
            return JsonResponse({'error': errors}, status=400)

        username = data['username']
        #make email an optional login input
        email = data.get('email', '').strip().lower() 
        password = data['password']

        user = UserProfile.objects.filter(username=username).first() or \
               UserProfile.objects.filter(email=email).first()

        if user:
            if check_password(password, user.password):
                return JsonResponse({'message': 'Login successful', 'user': {'id': user.id, 'username': user.username}})
            else:
                return JsonResponse({'error': 'Invalid credentials'}, status=400)

        return JsonResponse({'error': 'User not found'}, status=400)

#CLOTHING LIST VIEW
class ClothingListView(APIView):
    # declare parsers to allow file uploads
    parser_classes = [MultiPartParser, FormParser]

    # list all clothing items
    def get(self, request):
        try:
            clothing_items = Clothing.objects.all()
            serializer = ClothingSerializer(clothing_items, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Failed to fetch clothing items: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        #retrieves the image from the frontend request
        image_file = request.FILES.get('image')
        if not image_file:
            return Response({"error": "Image is required"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ClothingSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            #return the clothing item as an object
            clothing_item = serializer.save()
            #process the keypoints
            try:
                resize_saved_image(clothing_item.image.path, output_size=(300, 300))
                #method from utils
                keypoints, descriptors = orb_keypoint_detection(clothing_item.image.path)
                if descriptors is not None:
                    #save the keypoint descriptors in the Clothing model
                    clothing_item.keypoint_value = descriptors.tobytes()
                    clothing_item.save(update_fields=['keypoint_value'])
                else:
                    return Response({"warning": "Image uploaded, but no features were detected."}, status=status.HTTP_201_CREATED)  # no descriptors found
                return Response(ClothingSerializer(clothing_item).data, status=status.HTTP_201_CREATED)

            except Exception as img_process_error:
                clothing_item.delete()  # Rollback: delete the saved item if image processing failed
                return Response({"error": f"Error processing image: {str(img_process_error)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as save_error:
            return Response({"error": f"Error saving clothing item: {str(save_error)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#WISHLIST VIEWS
@api_view(['GET'])
def check_wishlist_status(request, item_id):
    user_id = request.GET.get('user_id')
    if not user_id:
        return Response({'error': 'Missing user_id'}, status=400)

    is_favourited = Wishlist.objects.filter(user_id=user_id, item_id=item_id).exists()
    return Response({'is_favourited': is_favourited})


@api_view(['POST'])
def add_to_wishlist(request):
    user_id = request.data.get('user_id')
    item_id = request.data.get('item_id')
    if not (user_id and item_id):
        return Response({'error': 'Missing user_id or item_id'}, status=400)

    Wishlist.objects.get_or_create(user_id=user_id, item_id=item_id)
    return Response({'status': 'added'})


@api_view(['POST'])
def remove_from_wishlist(request):
    user_id = request.data.get('user_id')
    item_id = request.data.get('item_id')
    if not (user_id and item_id):
        return Response({'error': 'Missing user_id or item_id'}, status=400)

    Wishlist.objects.filter(user_id=user_id, item_id=item_id).delete()
    return Response({'status': 'removed'})


@api_view(['GET'])
def get_user_wishlist(request):
    user_id = request.GET.get('user_id')
    if not user_id:
        return Response({'error': 'Missing user_id'}, status=400)

    items = Clothing.objects.filter(wishlist__user_id=user_id)
    serializer = ClothingSerializer(items, many=True)
    return Response(serializer.data)

#GET USER DETAILS FOR PROFILE PERSONALISATION
@api_view(['GET'])
def get_user_by_id(request, user_id):
    try:
        user = UserProfile.objects.get(pk=user_id)
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
        })
    except UserProfile.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)
    

