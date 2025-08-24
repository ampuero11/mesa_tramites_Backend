from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.utils import timezone
from django.conf import settings
from django.template.loader import render_to_string

from .models import Record, RecordDetail
from .serializers import RecordSerializer

from requests_app.models import Request
from mesa_partes.utils.response import custom_response

import weasyprint
import os

class RecordViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'], url_path='generar')
    def generar_acta(self, request):
        today = timezone.localdate()
        tramites_hoy = Request.objects.filter(created_at__date=today)

        if not tramites_hoy.exists():
            return Response({"detail": "No hay trámites registrados hoy."}, status=status.HTTP_400_BAD_REQUEST)

        record = Record.objects.create(
            date=today,
            description=f"Acta de trámites del {today.strftime('%d/%m/%Y')}",
            created_by=request.user
        )

        for t in tramites_hoy:
            RecordDetail.objects.create(
                record=record,
                request=t
            )

        html = render_to_string('acta.html', {'today': today, 'tramites': tramites_hoy})
        pdf_file = weasyprint.HTML(string=html).write_pdf()

        filename = f"acta_{today}.pdf"
        file_path = os.path.join(settings.MEDIA_ROOT, 'records', filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as f:
            f.write(pdf_file)

        record.file.name = f"records/{filename}"
        record.save()

        pdf_url = request.build_absolute_uri(record.file.url)
        return Response(custom_response({
            "type": "success",
            "dto": {"id": str(record.id), "file_url": pdf_url},
            "listMessages": ["Acta generada correctamente"]
        }))

    @action(detail=False, methods=['get'], url_path='listar')
    def list_records(self, request):
        queryset = Record.objects.all().order_by('-date')
        serializer = RecordSerializer(queryset, many=True)
        return Response(custom_response({
            "type": "success",
            "dto": serializer.data,
            "listMessages": ["Listado de actas obtenido correctamente"]
        }))