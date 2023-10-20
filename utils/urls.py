from django.urls import path, include
from .views import (
    SuggestedTimeSlotsView,
)

urlpatterns = [
    path("suggested-times/", SuggestedTimeSlotsView.as_view()),
]
