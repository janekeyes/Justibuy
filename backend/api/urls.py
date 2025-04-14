from django.urls import path
from .views import RegisterUser, login_user, ClothingListView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/', RegisterUser, name='register'),
    path('login/', login_user, name='login'),
    path('clothing/', ClothingListView.as_view(), name='clothing-list'),  # Use class-based view here
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

