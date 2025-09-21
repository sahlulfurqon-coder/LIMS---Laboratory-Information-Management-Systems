# lims_backend/accounts/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, ProfileView, LogoutView, MyTokenObtainPairView, UserViewSet
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth-register'),        # POST (Admin)
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),  # POST
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # POST
    path('logout/', LogoutView.as_view(), name='auth-logout'),              # POST
    path('profile/', ProfileView.as_view(), name='auth-profile'),           # GET, PUT
    path('', include(router.urls)),                                         # /users/
]
