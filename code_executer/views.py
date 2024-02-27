import io
import sys
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Code
from .serializers import CodeSerializer


class CodeView(APIView):
    serializer_class = CodeSerializer
    queryset = Code.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = CodeSerializer(data=request.data)
        if serializer.is_valid():
            code_obj = serializer.save()
            code_to_execute = serializer.validated_data['code']
            print("--------------------------------")

            old_stdout = sys.stdout
            redirected_output = sys.stdout = io.StringIO()

            try:
                exec(code_to_execute)
                exec_output = redirected_output.getvalue()
                response_data = {
                    "code": code_to_execute,
                    "output": exec_output
                }
                print("-------------------------------")
                print("code:", response_data['code'])
                return Response(response_data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            finally:
                sys.stdout = old_stdout
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
