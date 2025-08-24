from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import CustomTokenObtainPairSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from mesa_partes.utils.response import custom_response
from rest_framework import status

class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class CustomRefreshView(TokenRefreshView):

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            data = custom_response(
                type="error",
                dto=None,
                listMessages=[str(e)]
            )
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        response_data = custom_response(
            type="success",
            dto=serializer.validated_data,
            listMessages=["Token refrescado correctamente"]
        )
        return Response(response_data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = custom_response(
            type="success",
            dto=None,
            listMessages=["Sesión cerrada correctamente"]
        )
        return Response(data)
