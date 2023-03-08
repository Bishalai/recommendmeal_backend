from django.urls import path, include
from .views import ProfileListView, UsersListView, SignUpView, SignInView, SignOutView, GetHistoryView
from .views import RecommendMealView, UserDetails, GetCSRFToken, CheckAuthenticatedView, RateMealView

urlpatterns = [
    path('profiles', ProfileListView.as_view()),
    path('users', UsersListView.as_view()),
    path('signup',SignUpView.as_view()),
    path('signin',SignInView.as_view()),
    path('signout',SignOutView.as_view()),
    path('userdetails', UserDetails.as_view()),
    path('csrf_cookie',GetCSRFToken.as_view()),
    path('authenticated',CheckAuthenticatedView.as_view()),
    path('recommended',RecommendMealView.as_view()),
    path('ratemeal',RateMealView.as_view()),
    path('gethistory',GetHistoryView.as_view())
]