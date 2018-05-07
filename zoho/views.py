import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from zoho.event_handlers import subscription_created, invoice_created


@csrf_exempt
@require_POST
def update_chart_mogul(request):
    data = request.POST["payload"]
    payload = json.loads(data)

    if payload["event_type"] == "subscription_created":
        subscription_created(payload)
    if payload["event_type"] == "invoice_notification":
        invoice_created(payload)

    # TODO: Support other webhook events

    return JsonResponse({"msg": "success"}, status=200)
