from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Garantia
from .serializers import GarantiaSerializer

class GarantiaViewSet(viewsets.ModelViewSet):
    queryset = Garantia.objects.all()
    serializer_class = GarantiaSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # Obtener parámetro sucursal (por nombre o por ID)
        sucursal_param = self.request.query_params.get("sucursal", "")

        if sucursal_param:
            # Intentar filtrar primero por ID
            if sucursal_param.isdigit():
                queryset = queryset.filter(sucursal_id=sucursal_param)
            else:
                # Si no es número, filtrar por nombre
                queryset = queryset.filter(sucursal__nombre__icontains=sucursal_param)

        return queryset

