from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
import json
from .models import UserProfile, Clothing
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ClothingSerializer
from .utils import orb_keypoint_detection
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

@api_view(['POST'])
def user_image_process(request):
    try:
        # gets the user uploaded image as base 64
        user_image_data = request.data.get('image')
        if not user_image_data:
            return Response({'error': 'Could not find image'}, status=400)
        
        #call method from utils
        keypoints, _ = orb_keypoint_detection(user_image_data, is_base64=True)

        #return the number of keypoints detected
        return Response({
            'keypoints_detected': len(keypoints)

        })
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    





# Register view with password hashing
@csrf_exempt
def RegisterUser(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username', '').strip()
            email = data.get('email', '').strip().lower()
            password = data.get('password', '')

            if not username or not email or not password:
                return JsonResponse({'error': 'All fields are required'}, status=400)

            # Check if username or email already exists
            if UserProfile.objects.filter(username=username).exists():
                return JsonResponse({'error': 'Username already exists'}, status=400)
            if UserProfile.objects.filter(email=email).exists():
                return JsonResponse({'error': 'Email already exists'}, status=400)

            # Hash password and create user
            hashed_password = make_password(password)
            user = UserProfile(username=username, email=email, password=hashed_password)
            user.save()

            return JsonResponse({'message': 'User registered successfully'}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)  # Handle GET requests

# Login view with password checking
@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email', '').strip().lower()  # Convert email to lowercase
        password = data['password']

        # Find user by username or email
        user = UserProfile.objects.filter(username=username).first() or \
               UserProfile.objects.filter(email=email).first()

        if user:
            # Check if the password matches the hashed password stored in the database
            if check_password(password, user.password):
                return JsonResponse({'message': 'Login successful', 'username': user.username})
            else:
                return JsonResponse({'error': 'Invalid credentials'}, status=400)
        
        return JsonResponse({'error': 'User not found'}, status=400)

class ClothingListView(APIView):
    #declare parsers to allow file uploads
    parser_classes = [MultiPartParser, FormParser]
    def get(self, request):
        clothing_items = Clothing.objects.all()
        serializer = ClothingSerializer(clothing_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        #retrives the image from the frontend request
        image_file = request.FILES.get('image')
        if not image_file:
            return Response ({"error" : "Image file is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            serializer = ClothingSerializer(data=request.data)
            if serializer.is_valid():
                #return the clothin item as an object
                clothing_item = serializer.save()
                #process the keypoints
                try:
                    #method from utils
                    keypoints, descriptors = orb_keypoint_detection(clothing_item.image.path, is_base64=False)
                    if descriptors is not None:
                        #save the keypoint descriptors in the Clothing model
                        clothing_item.keypoint_value = descriptors.tobytes()
                        clothing_item.save(update_fields=['keypoint_value'])

                except Exception as e:
                    return Response({"error": f"Error processing image: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
                    return Response({"error": f"Error saving image: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


