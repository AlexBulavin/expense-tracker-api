from rest_framework import serializers
from restapi import models

class Expense(serializers.ModelSerializer):
    amount = serializers.FloatField(required=True)
    merchant = serializers.CharField(required=True) #max_lenght=255
    description = serializers.CharField(required=False)  # max_lenght=255
    category = serializers.CharField(required=True)  # max_lenght=255
    date_created = serializers.DateTimeField(required=False)
    date_updated = serializers.DateTimeField(required=False)

    class Meta:
        model = models.Expense
        fields = '__all__'
        read_only_fields = ['id', 'date_created', 'date_updated']
