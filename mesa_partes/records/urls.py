from django.urls import path
from .viewsets import RecordViewSet

record_generate = RecordViewSet.as_view({'post': 'generar_acta'})
record_list = RecordViewSet.as_view({'get': 'list_records'})

urlpatterns = [
    path("records/generar/", record_generate, name="generar_acta"),
    path("records/", record_list, name="list_records"),
]
