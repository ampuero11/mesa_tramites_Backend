from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import AdminUser
from django.contrib.auth import authenticate
from mesa_partes.utils.response import custom_response

class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminUser
        fields = ["id", "name", "email"]
        read_only_fields = ["id"]

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = "email"

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError("Credenciales inválidas")

        data = super().validate(attrs)

        response_data = custom_response(
            type="success",
            dto={
                "access": data["access"],
                "refresh": data["refresh"],
                "email": user.email,
            },
            listMessages=["Login exitoso"]
        )

        return response_data