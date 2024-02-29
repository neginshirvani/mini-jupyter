import io
import sys
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Code
from .serializers import CodeSerializer
import requests
import json


class CodeView(APIView):
    serializer_class = CodeSerializer
    queryset = Code.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = CodeSerializer(data=request.data)
        if serializer.is_valid():
            code_obj = serializer.save()
            code_to_execute = serializer.validated_data['code']
            notebook_url = "http://localhost:8888"
            token = "your_token_here"  # Replace with your Jupyter token

            # Headers for the HTTP requests
            headers = {
                "Authorization": f"token {token}",
                "Content-Type": "application/json"
            }

            create_response = requests.post(
                f"{notebook_url}/api/contents",
                headers=headers,
                data=json.dumps({
                    "type": "notebook",
                    "content": {
                        "cells": [{
                            "cell_type": "code",
                            "metadata": {},
                            "execution_count": None,
                            "source": ["print('Hello, Jupyter!')"],  # Your Python code here
                            "outputs": []
                        }],
                        "metadata": {},
                        "nbformat": 4,
                        "nbformat_minor": 2
                    }
                })
            )

            if create_response.status_code == 201:
                notebook_data = create_response.json()
                notebook_path = notebook_data["path"]
                print(f"Notebook created: {notebook_path}")

                # Example of executing the first cell in the newly created notebook
                # You might need to adjust this part to fit your needs
                execute_response = requests.post(
                    f"{notebook_url}/api/contents/{notebook_path}/execute",
                    headers=headers
                )
                if execute_response.status_code == 200:
                    return Response(execute_response.content, status=status.HTTP_200_OK)
                else:
                    return Response(execute_response.text, status=execute_response.status_code)
            else:
                return Response(create_response.text, status=create_response.status_code)
