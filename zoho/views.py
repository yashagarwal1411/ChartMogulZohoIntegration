from django.shortcuts import render

# Create your views here.

import chartmogul


chart_mogul_account_token = "ef93433271637296bbb960c8e664b0bc"
chart_mogul_secret_key = "f3184442edb612acf395e0807a4f1c55"

config = chartmogul.Config(chart_mogul_account_token, chart_mogul_secret_key)


def new_subscription(request):
    plan_data = {
        'name': 'Awesome plan'
    }
    chartmogul.Plan.create(config, data=plan_data).get()
