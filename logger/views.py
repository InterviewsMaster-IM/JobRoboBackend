from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import LogEntry
import json


@csrf_exempt
@require_http_methods(["POST"])
def log_entries(request):
    try:
        logs = json.loads(request.body)
        for log in logs:
            LogEntry.objects.create(
                level=log.get('level'),
                message=log.get('message'),
                data=log.get('data', log))
        return JsonResponse({"status": "success"}, status=201)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
