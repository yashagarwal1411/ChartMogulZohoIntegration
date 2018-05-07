from datetime import datetime
import re

from zoho.models import Customer, Plan
from zoho.chartmogul_api_helpers import create_customer, create_plan, create_invoice


def subscription_created(payload):
    """
    Creates a customer and plan on ChartMogul
    :param payload:
    :return:
    """

    # TODO: Parse data using Serializers instead

    subscription = payload["data"]["subscription"]
    customer = subscription["customer"]
    plan = subscription["plan"]

    existing_customer = Customer.objects.filter(zoho_id=customer["customer_id"]).first()

    if not existing_customer:
        chartmogul_customer = create_customer(customer["customer_id"],customer["first_name"])
        Customer.objects.create(zoho_id=customer["customer_id"], chartmogul_id=chartmogul_customer.uuid)

    existing_plan = Plan.objects.filter(zoho_id=plan["plan_id"])

    if not existing_plan:
        interval_unit = subscription["interval_unit"]
        interval_count= subscription["interval"]

        interval_unit, interval_count = clean_up_intervals(interval_unit, interval_count)
        chartmogul_plan = create_plan(plan["name"], interval_count, interval_unit, plan["plan_id"])
        Plan.objects.create(zoho_id=plan["plan_id"], chartmogul_id=chartmogul_plan.uuid)


def invoice_created(payload):
    """
    Creates a invoice on ChartMogul
    :param payload:
    :return:
    """

    # TODO: Parse data using Serializers instead

    invoice = payload["data"]["invoice"]
    zoho_customer_id = invoice["customer_id"]
    existing_customer = Customer.objects.filter(zoho_id=zoho_customer_id).get()

    zoho_plan_id = invoice["invoice_items"][0]["product_id"]
    existing_plan = Plan.objects.filter(zoho_id=zoho_plan_id).get()

    service_period_string = invoice["invoice_items"][0]["description"]

    service_period_start, service_period_end = get_service_periods(service_period_string)

    create_invoice(existing_customer.chartmogul_id, invoice["number"], invoice["invoice_date"] + " 00:00:00",
                   invoice["due_date"] + " 00:00:00", invoice["subscriptions"][0]["subscription_id"],
                   existing_plan.chartmogul_id, service_period_start, service_period_end,
                   invoice["invoice_items"][0]["price"] * 100, invoice["payments"][0]["date"] + "T00:00:00")


def clean_up_intervals(interval_unit, interval_count):
    """

    :param interval_unit:
    :param interval_count:
    :return:
    """
    if interval_unit == "months":
        interval_unit = "month"
    if interval_unit == "weeks":
        interval_unit = "day"
        interval_count = interval_count * 7
    if interval_unit == "years":
        interval_unit = "year"
    return interval_unit, interval_count


def get_service_periods(service_period_string):
    """

    :param service_period_string:
    :return:
    """
    service_period_start, service_period_end = re.match(".*\\(from (.*) to (.*) \\)", service_period_string).groups()
    service_period_start = datetime.strptime(service_period_start, '%d-%B-%Y').strftime('%Y-%m-%d') + " 00:00:00"
    service_period_end = datetime.strptime(service_period_end, '%d-%B-%Y').strftime('%Y-%m-%d') + " 00:00:00"

    return service_period_start, service_period_end
