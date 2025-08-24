from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import RequestCreateSerializer, RequestSerializer
from mesa_partes.utils.response import custom_response
from django.core.mail import send_mail
from django.conf import settings

class RequestViewSet(viewsets.ViewSet):
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request):
        serializer = RequestCreateSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()

            try:
                send_mail(
                    subject=f"Trámite recibido: {instance.code}",
                    message=f"Hola {instance.full_name}, tu trámite ha sido registrado correctamente. Código: {instance.code}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[instance.email],
                    fail_silently=False,
                )
                email_messages = ["Correo de confirmación enviado correctamente"]
            except Exception as e:
                email_messages = [f"No se pudo enviar correo: {str(e)}"]

            data = custom_response(
                type="success",
                dto=RequestSerializer(instance).data,
                listMessages=["Trámite registrado correctamente"] + email_messages
            )

            return Response(data, status=status.HTTP_201_CREATED)

        errors = [f"{k}: {', '.join(v)}" for k, v in serializer.errors.items()]
        return Response(custom_response(type="error", dto=None, listMessages=errors), status=status.HTTP_400_BAD_REQUEST)
