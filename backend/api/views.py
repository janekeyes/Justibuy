from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
import json
from .models import UserProfile, ClothingItem
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ClothingItemSerializer


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


# Get clothing items view using Django Rest Framework
class ClothingItemListView(APIView):
    def get(self, request, *args, **kwargs):
        items = ClothingItem.objects.all()  # Query all clothing items from the database
        serializer = ClothingItemSerializer(items, many=True)  # Serialize the items
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        # Handle POST requests to create a new clothing item
        data = request.data  # Automatically parses JSON data
        serializer = ClothingItemSerializer(data=data)

        if serializer.is_valid():
            serializer.save()  # Save the new clothing item
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

