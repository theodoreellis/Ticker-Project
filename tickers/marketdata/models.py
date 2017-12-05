from django.db import models
import requests
import json

class Ticker(models.Model):
    symbol = models.CharField('Stock Symbol',max_length=10)
    price = models.FloatField('Most Recent Price',default=0)
