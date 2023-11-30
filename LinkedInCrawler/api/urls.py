from django.urls import path, include
from .views import *
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView



urlpatterns = [
   path("linkedin-user/all", LinkedinUsersView.as_view(), name="linkedin_user_all"),
   path("linkedin-user/<int:pk>", LinkedinUserView.as_view(), name="linkedin_user_id"),
   path("linkedin-user/key-filter/<str:key>", LinkedinUserKeyFilterView.as_view(), name="linkedin_user_key_filter"),

   path("linkedin-user/detail/<int:pk>", LinkedinUserDetailView.as_view(), name="linkedin_user_detail"),
   path("linkedin-user/detail/all", LinkedinUsersDetailView.as_view(), name="linkedin_user_detail_all"),

   path("token/obtain", TokenObtainPairView.as_view(), name="token_obtain"),
   path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
]