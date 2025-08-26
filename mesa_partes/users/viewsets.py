from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import CustomTokenObtainPairSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from mesa_partes.utils.response import custom_response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()

class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class CustomRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            data = custom_response(
                type="error",
                dto=None,
                listMessages=["No se envió el token de refresh"]
            )
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        try:
            refresh = RefreshToken(refresh_token)
            access = str(refresh.access_token)

            try:
                user = refresh.user
            except AttributeError:
                user_id = refresh["user_id"]
                user = User.objects.get(id=user_id)

            dto = {
                "access": access,
                "refresh": str(refresh),
                "email": user.email,
            }

            data = custom_response(
                type="success",
                dto=dto,
                listMessages=["Token refrescado correctamente"]
            )
            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            data = custom_response(
                type="error",
                dto=None,
                listMessages=[str(e)]
            )
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = custom_response(
            type="success",
            dto=None,
            listMessages=["Sesión cerrada correctamente"]
        )
        return Response(data)
