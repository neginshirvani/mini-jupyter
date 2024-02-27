from django.urls import path
from .views import *

urlpatterns = [
    path('code/', CodeView.as_view()),
]
