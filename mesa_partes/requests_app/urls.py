from django.urls import path
from .viewsets import RequestAdminViewSet

request_admin_list = RequestAdminViewSet.as_view({'get': 'list'})
request_admin_detail = RequestAdminViewSet.as_view({'get': 'retrieve'})
request_admin_send_response = RequestAdminViewSet.as_view({'post': 'send_response'})
request_admin_change_status = RequestAdminViewSet.as_view({'patch': 'change_status'})

urlpatterns = [
    path("tramites/", RequestAdminViewSet.as_view({'post': 'create'}), name="register_request"),

    path("admin/tramites/", request_admin_list, name="admin_tramites_list"),
    path("admin/tramites/<uuid:pk>/", request_admin_detail, name="admin_tramites_detail"),
    path("admin/tramites/<uuid:pk>/respuesta/", request_admin_send_response, name="admin_tramites_send_response"),
    path("admin/tramites/<uuid:pk>/estado/", request_admin_change_status, name="admin_tramites_change_status"),
]
