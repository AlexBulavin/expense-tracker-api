from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from restapi import models
from django.forms.models import model_to_dict


# Create your views here.
class ExpenseListCreate(APIView):
    def get(self, request):
        expenses = models.Expense.objects.all()
        all_expenses = [model_to_dict(expenses) for expense in expenses] # Извлекаем поэлементно
        return Response(all_expenses, status=200)

    def post(self, request):
        # Извлекаем данные одни за другими из payload и сохраняем в переменных.
        amount = request.data['amount']
        merchant = request.data['merchant']
        description = request.data['description']
        category = request.data['category']
        # date_created = request.data['date_created']
        # date_updated = request.data['date_updated']

        expense = models.Expense.objects.create(amount=amount, merchant=merchant, description=description, category=category, )

        return Response(model_to_dict(expense), status=201)
