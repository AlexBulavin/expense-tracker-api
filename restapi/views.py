# from django.shortcuts import render
# from rest_framework.views import APIView
# from rest_framework.response import Response
from restapi import models, serializers
from rest_framework.generics import RetrieveDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_api_key.permissions import HasAPIKey
# from django.forms.models import model_to_dict

# Create your views here.
class ExpenseListCreate(ListCreateAPIView):

    # Старый метод через APIView
    # def get(self, request):
    #     #Делаем сериализатор
    #     expenses = models.Expense.objects.all()
    #     serializer = serializers.Expense(expenses, many=True)
    #
    #     return Response(serializer.data, status=200)
    #
    # def post(self, request):
    #     # Реализация без сериализатора:
    #     # # Извлекаем данные одни за другими из payload и сохраняем в переменных.
    #     # amount = request.data['amount']
    #     # merchant = request.data['merchant']
    #     # description = request.data['description']
    #     # category = request.data['category']
    #     # # date_created = request.data['date_created']
    #     # # date_updated = request.data['date_updated']
    #     #
    #     # expense = models.Expense.objects.create(amount=amount, merchant=merchant, description=description, category=category, )
    #
    #     #Реализация с сериализатором:
    #     serializer = serializers.Expense(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #
    #     return Response(serializer.data, status=201)
    serializer_class = serializers.Expense
    queryset = models.Expense.objects.all()
    filterset_fields = ['category', 'merchant']
    permission_classes = [HasAPIKey] #Проверяем аутентификацию пользователя

class ExpenseRetrieveDelete(RetrieveDestroyAPIView):
    # def get(self, request, pk):
    #     return Response()
    #
    # def delete(self, request):
    #     return Response()

    serializer_class = serializers.Expense
    queryset = models.Expense.objects.all()
    permission_classes = [HasAPIKey]  # Проверяем аутентификацию пользователя