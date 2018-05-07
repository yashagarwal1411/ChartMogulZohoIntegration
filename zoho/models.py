from django.db import models


class Customer(models.Model):
    """
    Table for mapping zoho customer id and chart mogul customer id
    """
    zoho_id = models.CharField(max_length=255)
    chartmogul_id = models.CharField(max_length=255)


class Plan(models.Model):
    """
    Table for mapping zoho plan id and chart mogul plan id
    """
    zoho_id = models.CharField(max_length=255)
    chartmogul_id = models.CharField(max_length=255)