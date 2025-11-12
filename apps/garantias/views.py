from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Garantia
from .serializers import GarantiaSerializer

class GarantiaViewSet(viewsets.ModelViewSet):
    queryset = Garantia.objects.all()
    serializer_class = GarantiaSerializer
