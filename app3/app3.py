from django.http import JsonResponse
import time
from django.views.decorators.csrf import csrf_exempt
import json

def get_api(request):
    time.sleep(0.1)  # Simulating moderate scalability
    return JsonResponse({"message": "Hello from Django App!"})

@csrf_exempt
def post_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        time.sleep(0.1)  # Simulating moderate scalability
        return JsonResponse(data, status=201)
    return JsonResponse({"message": "Invalid request"}, status=400)
