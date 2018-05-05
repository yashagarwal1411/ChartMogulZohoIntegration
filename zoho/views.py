from django.http import JsonResponse
from django.shortcuts import render
import json

# Create your views here.

import chartmogul
from django.views.decorators.csrf import csrf_exempt

chart_mogul_account_token = "ef93433271637296bbb960c8e664b0bc"
chart_mogul_secret_key = "f3184442edb612acf395e0807a4f1c55"

zoho_client_id="1000.RV61VOE3HPHB55800RNPYVUME6GULW"
zoho_client_secret="59de843034067a4f275e74f4263d47252afa1b8372"

config = chartmogul.Config(chart_mogul_account_token, chart_mogul_secret_key)


@csrf_exempt
def zoho(request):

    if request.body:
        data = request.body.decode('utf-8')
        print("DATA")
        print(data)
        print(type(data))
        received_json_data = json.loads(data)
        print(json.dumps(received_json_data))
    return JsonResponse({"msg": "success"}, status=200)
    # plan_data = {
    #     'name': 'Awesome plan'
    # }
    # chartmogul.Plan.create(config, data=plan_data).get()


# def oauth2callback(request):
