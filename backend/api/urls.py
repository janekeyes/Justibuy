from django.urls import path
from .views import RegisterUser, login_user, ClothingListView, ClothingSearchView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/', RegisterUser, name='register'),
    path('login/', login_user, name='login'),
    path('clothing/', ClothingListView.as_view(), name='clothing-list'),  
    path('search-clothing/', ClothingSearchView.as_view(), name='search-clothing'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

