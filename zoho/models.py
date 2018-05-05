from django.db import models


class Customer(models.Model):
    zoho_id = models.CharField(max_length=255)
    chartmogul_id = models.CharField(max_length=255)


class Plan(models.Model):
    zoho_id = models.CharField(max_length=255)
    chartmogul_id = models.CharField(max_length=255)