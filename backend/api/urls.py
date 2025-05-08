# this file is responsible for mapping url endpoints to their 
# view logic, routing frontend and API traffic apprropriatley 
# based on their request path

from django.urls import path
from .views import RegisterUser, login_user, ClothingListView, ClothingSearchView, ClothingDetailView, keyword_search, check_wishlist_status, add_to_wishlist, remove_from_wishlist, get_user_wishlist, get_user_by_id
from django.conf import settings
from django.conf.urls.static import static


#create the paths for all user requests
urlpatterns = [
    path('register/', RegisterUser, name='register'),
    path('login/', login_user, name='login'),
    path('clothing/', ClothingListView.as_view(), name='clothing-list'),  
    path('search-clothing/', ClothingSearchView.as_view(), name='search-clothing'),
    path('search-keyword/', keyword_search, name='search_by_keyword'),
    path('clothing/<int:pk>/', ClothingDetailView.as_view(), name='clothing-detail'),
    path('user/<int:user_id>/', get_user_by_id),
    path('wishlist/<int:item_id>/status/', check_wishlist_status),
    path('wishlist/add/', add_to_wishlist),
    path('wishlist/remove/', remove_from_wishlist),
    path('wishlist/', get_user_wishlist),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

