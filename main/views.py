from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_GET
from django.contrib.staticfiles.views import serve
import json
from rest_framework.response import Response

from rest_framework.views import APIView

from main import settings
import boto3 #pip install boto3

def globalConfigsView(request):
    try:
        # Open and read the JSON file
        with open("main/globalConfigs.json", "r") as fsock:
            data = json.load(fsock)  # Load the file contents as JSON

        # Return the data as a JSON response
        return JsonResponse(data, safe=False)
    
    except FileNotFoundError:
        return JsonResponse({"error": "File not found."}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Error decoding JSON."}, status=400)

@require_GET
def healthCheck(request):
    return JsonResponse({"result": True, "message": "Server is Up!", "version": "1.0.1"})

class UploadToS3(APIView):
    def post(self, request):
        file = request.FILES['file']
        filePath = request.POST.get('filePath')
        access_key = settings.AWS_ACCESS_KEY_ID
        access_secret_key = settings.AWS_SECRET_ACCESS_KEY
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME 

        try:
            client_s3 = boto3.client(
                's3',
                aws_access_key_id = access_key,
                aws_secret_access_key= access_secret_key
            )

            # Upload File
            client_s3.upload_fileobj(file, settings.AWS_STORAGE_BUCKET_NAME, filePath)

            url = f"https://{bucket_name}.s3.amazonaws.com/{filePath}"
            return Response({"success": True, "message": "File has been uploaded", "url": url})

        except Exception as e:
            return Response({"result": False, "message": f"File not upload cause: {e}", "url": None}, status=400)
