from django.urls import path, include
from .views import (
    SuggestedTimeSlotsAPIView,
)

urlpatterns = [
    path("suggested-times/", SuggestedTimeSlotsAPIView.as_view()),
]
