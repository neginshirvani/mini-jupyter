from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView

from rest_framework.response import Response
from rest_framework import status
import sys
import io

from .models import Code
from .serializers import CodeSerializer

class CodeView(CreateAPIView):
    serializer_class = CodeSerializer

