from django.conf import settings

import chartmogul

chartmogul_config = chartmogul.Config(settings.CHART_MOGUL["account_token"], settings.CHART_MOGUL["secret_key"])
zoho_data_source_uuid = settings.ZOHO["data_source_uuid"]