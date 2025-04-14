from django.urls import path
from api.views import RegisterUser, login_user, ClothingItemListView

urlpatterns = [
    path('register/', RegisterUser, name='register'),
    path('login/', login_user, name='login'),
    path('clothing-items/', ClothingItemListView.as_view(), name='clothing-items'),
]

