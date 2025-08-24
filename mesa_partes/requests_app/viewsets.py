from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.decorators import action

from django_filters.rest_framework import DjangoFilterBackend
from django.core.mail import send_mail
from django.conf import settings

from .serializers import RequestCreateSerializer, RequestSerializer, RequestStatus
from .models import Request

from responses.models import Response as ResponseModel
from responses.serializers import ResponseCreateSerializer

from mesa_partes.utils.response import custom_response

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

class RequestAdminViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Request.objects.all().prefetch_related('files', 'status_history')
    serializer_class = RequestSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'code', 'created_at']
    search_fields = ['full_name', 'email', 'concept']
    ordering_fields = ['created_at', 'code']
    ordering = ['-created_at']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        response_data = custom_response(
            type="success",
            dto=serializer.data,
            listMessages=["Listado de trámites obtenido correctamente"]
        )
        return Response(response_data)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        response_data = custom_response(
            type="success",
            dto=serializer.data,
            listMessages=["Detalle del trámite obtenido correctamente"]
        )
        return Response(response_data)

    @action(detail=True, methods=['patch'], url_path='estado')
    def change_status(self, request, pk=None):
        try:
            instance = self.get_object()
            new_status = request.data.get("status")
            if new_status not in [choice[0] for choice in instance.STATUS_CHOICES]:
                return Response(
                    custom_response(
                        type="error",
                        dto=None,
                        listMessages=["Estado inválido"]
                    ),
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            instance.status = new_status
            instance.save()

            RequestStatus.objects.create(
                request=instance,
                status=new_status,
                changed_by=request.user 
            )

            serializer = self.get_serializer(instance)
            return Response(
                custom_response(
                    type="success",
                    dto=serializer.data,
                    listMessages=[f"Estado actualizado a {new_status}"]
                )
            )

        except Request.DoesNotExist:
            return Response(
                custom_response(
                    type="error",
                    dto=None,
                    listMessages=["Trámite no encontrado"]
                ),
                status=status.HTTP_404_NOT_FOUND
            )
        
    @action(detail=True, methods=['post'], url_path='respuesta')
    def send_response(self, request, pk=None):
        instance = self.get_object()
        serializer = ResponseCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        response_instance = ResponseModel.objects.create(
            request=instance,
            admin=request.user,
            message=serializer.validated_data["message"],
            sent_email=True
        )

        send_mail(
            subject=f"Respuesta a su trámite {instance.code}",
            message=response_instance.message,
            from_email='no-reply@empresa.com',
            recipient_list=[instance.email],
            fail_silently=False
        )

        return Response(
            custom_response({
                "type": "success",
                "dto": {"id": str(response_instance.id), "message": response_instance.message},
                "listMessages": ["Respuesta enviada y registrada correctamente"]
            }),
            status=status.HTTP_201_CREATED
        )