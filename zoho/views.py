import binascii

from django.http import JsonResponse
from django.shortcuts import render
import json
from urllib.parse import parse_qs

# Create your views here.

import chartmogul
from django.views.decorators.csrf import csrf_exempt

from zoho.models import Customer, Plan

chart_mogul_account_token = "ef93433271637296bbb960c8e664b0bc"
chart_mogul_secret_key = "f3184442edb612acf395e0807a4f1c55"

zoho_client_id="1000.RV61VOE3HPHB55800RNPYVUME6GULW"
zoho_client_secret="59de843034067a4f275e74f4263d47252afa1b8372"

config = chartmogul.Config(chart_mogul_account_token, chart_mogul_secret_key)

zoho_data_source_uuid = "ds_d922a822-5090-11e8-afc6-5f5e6fd8a691"

@csrf_exempt
def zoho(request):
    if request.method == "POST":
        data = request.POST["payload"]
        payload = json.loads(data)

        if payload["event_type"] ==  "subscription_created":
            subscription_created(payload)
        if payload["event_type"] == "invoice_notification":
            invoice_created(payload)

    return JsonResponse({"msg": "success"}, status=200)


def subscription_created(payload):
    subscription = payload["data"]["subscription"]
    customer = subscription["customer"]
    plan = subscription["plan"]

    existing_customer = Customer.objects.filter(zoho_id=customer["customer_id"]).get()
    if not existing_customer:
        chartmogul_customer = chartmogul.Customer.create(config, data={
            "data_source_uuid": zoho_data_source_uuid,
            "external_id": customer["customer_id"],
            "name": customer["first_name"]
        }).get()
        print(chartmogul_customer)
        existing_customer = Customer.objects.create(zoho_id=customer["customer_id"], chartmogul_id=chartmogul_customer.uuid)

    existing_plan = Plan.objects.filter(zoho_id=plan["plan_id"])
    if not existing_plan:
        interval_unit = subscription["interval_unit"]
        interval_count= subscription["interval"]

        if interval_unit == "months":
            interval_unit = "month"
        if interval_unit == "weeks":
            interval_unit = "day"
            interval_count = interval_count*7
        if interval_unit == "years":
            interval_unit = "year"

        chartmogul_plan = chartmogul.Plan.create(config, data={
            "data_source_uuid": zoho_data_source_uuid,
            "name": plan["name"],
            "interval_count": interval_count,
            "interval_unit": interval_unit,
            "external_id": plan["plan_id"]
        }).get()

        existing_plan = Plan.objects.create(zoho_id=plan["plan_id"], chartmogul_id=chartmogul_plan.uuid)


def invoice_created(payload):
    invoice = payload["data"]["invoice"]
    zoho_customer_id = invoice["customer_id"]
    existing_customer = Customer.objects.filter(zoho_id=zoho_customer_id).get()

    zoho_plan_id = invoice["invoice_items"][0]["item_id"]
    existing_plan = Plan.objects.filter(zoho_id=zoho_plan_id).get()

    chartmogul.Invoice.create(
        config,
        uuid=existing_customer.chartmogul_id,
        data={
            "invoices": [
                {
                    "external_id": invoice["number"],
                    "date": invoice["invoice_date"] + " 00:00:00",
                    "currency": "USD",
                    "due_date": invoice["due_date"] + " 00:00:00",
                    "line_items": [
                        {
                            "type": "subscription",
                            "subscription_external_id": invoice["subscriptions"][0]["subscription_id"],
                            "plan_uuid": existing_plan.chartmogul_id,
                            "service_period_start": invoice["invoice_date"] + " 00:00:00",
                            "service_period_end": invoice["due_date"] + " 00:00:00",
                            "amount_in_cents": invoice["invoice_items"][0]["price"] * 100,
                        }
                    ],
                    "transactions": [
                        {
                            "date": invoice["payments"]["date"]+"T00:00:00",
                            "type": "payment",
                            "result": "successful"
                        }
                    ]
                }
            ]
        })


