from django.urls import path
from .api.views import MeView

urlpatterns = [
    path("me/", MeView.as_view(), name="api-me"),
]