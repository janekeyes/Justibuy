
**Developed by:** Jane Keyes  
**Course:** BSHCSD4  
**Supervisor:** William Clifford

---

## About

Justibuy is a mobile application that helps users find affordable fashion pieces by using image based & keyword based search features. Snap or upload a poto of a clothing item, and Justibuy will return similar clothing items sorted in ascending price order. Justibuy allows users to create wishlists too.

---

## Technology

### Frontend:
- [React Native](https://reactnative.dev/) 
- [Expo Router](https://expo.github.io/router/)
- Axios for API requests
- Global styling (generalStyles.tsx)

### Backend:
- [Django](https://www.djangoproject.com/) 
- Django REST Framework
- Python OpenCV (cv2) for ORB keypoint detection and matching
- PostgreSQL for persistent storage
- Media handling 

---

##  Starting out

### Django Backend

1. cd Justibuy/backend
2. pip install -r requirements.txt
3. python manage.py migrate
4. python manage.py runserver

#### React Native & Expo Frontend

1. cd Justibuy/MyApp
2. npm install
3. npx expo start

##### Running Tests
1. cd backend
2. python manage.py test api.tests.class_tests.ClothingSerializerTest
3. python manage.py test api.tests.class_tests.UserAuthTests
4. python manage.py test api.tests.system_tests.AuthorisedUserTests
5. python manage.py test api.tests.system_tests.ValidImageSearchTest


