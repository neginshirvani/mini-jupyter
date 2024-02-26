from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import sys
import io

class ExecuteCode(APIView):
    def post(self, request, *args, **kwargs):
        code = request.data.get('code', '')

        # Redirect stdout
        backup = sys.stdout
        sys.stdout = io.StringIO()

        try:
            exec(code)
            output = sys.stdout.getvalue()
        except Exception as e:
            output = str(e)
        finally:
            sys.stdout.close()
            sys.stdout = backup

        return Response({"output": output}, status=status.HTTP_200_OK)
