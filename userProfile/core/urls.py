from django.urls import path, include
from .views import ProfileListView, UsersListView, SignUpView, SignInView, SignOutView, GetHistoryView
from .views import RecommendMealView, UserDetails, RateMealView 
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('profiles', ProfileListView.as_view()),
    path('users', UsersListView.as_view()),
    path('signup',SignUpView.as_view()),
    path('signin',SignInView.as_view()),
    path('signout',SignOutView.as_view()),
    path('userdetails', UserDetails.as_view()),
    path('recommended',RecommendMealView.as_view()),
    path('ratemeal',RateMealView.as_view()),
    path('gethistory',GetHistoryView.as_view()),
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]