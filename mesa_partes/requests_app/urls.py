from django.urls import path
from .viewsets import RequestViewSet

urlpatterns = [
    path("tramites/", RequestViewSet.as_view({'post': 'create'}), name="register_request"),
]
