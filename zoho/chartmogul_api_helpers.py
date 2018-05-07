import chartmogul

from zoho.constants import chartmogul_config, zoho_data_source_uuid


def create_customer(zoho_customer_id, first_name):
    """

    :param zoho_customer_id:
    :param first_name:
    :return:
    """
    return chartmogul.Customer.create(chartmogul_config, data={
        "data_source_uuid": zoho_data_source_uuid,
        "external_id": zoho_customer_id,
        "name": first_name
    }).get()


def create_plan(name, interval_count, interval_unit, zoho_plan_id):
    """

    :param name:
    :param interval_count:
    :param interval_unit:
    :param zoho_plan_id:
    :return:
    """
    return chartmogul.Plan.create(chartmogul_config, data={
        "data_source_uuid": zoho_data_source_uuid,
        "name": name,
        "interval_count": interval_count,
        "interval_unit": interval_unit,
        "external_id": zoho_plan_id
    }).get()


def create_invoice(chartmogul_customer_id, zoho_invoice_id, invoice_date, invoice_due_date, zoho_subscription_id,
                   chartmogul_plan_id, service_period_start, service_period_end, amount_in_cents, payment_date):
    """

    :param chartmogul_customer_id:
    :param zoho_invoice_id:
    :param invoice_date:
    :param invoice_due_date:
    :param zoho_subscription_id:
    :param chartmogul_plan_id:
    :param service_period_start:
    :param service_period_end:
    :param amount_in_cents:
    :param payment_date:
    :return:
    """
    return chartmogul.Invoice.create(
        chartmogul_config,
        uuid=chartmogul_customer_id,
        data={
            "invoices": [
                {
                    "external_id": zoho_invoice_id,
                    "date": invoice_date,
                    "currency": "USD",
                    "due_date": invoice_due_date,
                    "line_items": [
                        {
                            "type": "subscription",
                            "subscription_external_id": zoho_subscription_id,
                            "plan_uuid": chartmogul_plan_id,
                            "service_period_start": service_period_start,
                            "service_period_end": service_period_end,
                            "amount_in_cents": amount_in_cents,
                        }
                    ],
                    "transactions": [
                        {
                            "date": payment_date,
                            "type": "payment",
                            "result": "successful"
                        }
                    ]
                }
            ]
        }).get()