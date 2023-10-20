from django.urls import path, include
from .views import (
    SignInView,
    SignUpView,
    UpdateUserView,
    DeleteUserView,
    UserDetailView,
    UpdateUserTimePreferenceView,
    UserTimePreferenceDetailView,
)

user_time_preference_urls = [
    path('update/', UpdateUserTimePreferenceView.as_view()),
    path('detail/', UserTimePreferenceDetailView.as_view()),
]

urlpatterns = [
    path('signup/', SignUpView.as_view()),
    path('signin/', SignInView.as_view()),
    path('update/', UpdateUserView.as_view()),
    path('delete/', DeleteUserView.as_view()),
    path('detail/', UserDetailView.as_view()),
    path('time-preference/', include(user_time_preference_urls)),
]