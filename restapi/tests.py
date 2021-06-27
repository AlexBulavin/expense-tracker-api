from django.test import TestCase
from restapi import models
from django.urls import reverse
# from django.db.models import Count

#from unittest import TestCase

# Create your tests here.
# # Предположм, что мы имеем для тестирования функцию, которая на вход получает два арнумента, а на выходе выдаёт их сумму
# def two_integers_sum(a, b):
#     return a+b
#
# class TestSum(TestCase):
#     def test_sum(self):
#         # Проверяем на конкретном примере, если результат выполнения функции two_integers_sum(1,2) равен 3
#         self.assertEqual(two_integers_sum(1, 2), 3)
class TestModels(TestCase):
    def test_expense(self):
        expense = models.Expense.objects.create(amount=249.99, merchant='amazon', description='anc headphones', category='music')
        inserted_expense = models.Expense.objects.get(pk=expense.id)

        self.assertEqual(249.99, inserted_expense.amount)
        self.assertEqual('amazon', inserted_expense.merchant)
        self.assertEqual('anc headphones', inserted_expense.description)
        self.assertEqual('music', inserted_expense.category)

class TestViews(TestCase):
    def test_expense_create(self):
        # Создаём тестовые данные
        payload = {
            'amount': 50.0,
            'merchant': 'AT&T',
            'description': 'cell phone supscription',
            'category': 'utilities'
        }
        # Сохраняем публикацию в переменную res
        res = self.client.post(reverse('restapi:expense-list-create'), payload, format='json')

        # Сравниваем код статуса созданного ресурса (доступности). Он должен быть 201
        self.assertEqual(201, res.status_code)

        # Проверяем ответ. Извлекаем данные и сравниваем их с тестовыми.
        json_res = res.json()

        self.assertEqual(payload['amount'], json_res['amount'])
        self.assertEqual(payload['merchant'], json_res['merchant'])
        self.assertEqual(payload['description'], json_res['description'])
        self.assertEqual(payload['category'], json_res['category'])
        self.assertIsInstance(json_res['id'], int) # Проверяем, целочисленное ли значение ID

    def test_expense_list(self):
        res = self.client.get(reverse('restapi:expense-list-create'), format='json')
        # Первая проверка - смотрим имеются ли данные в res
        self.assertEqual(200, res.status_code)

        json_res = res.json()

        # Проверяем, является ли json_res списком
        self.assertIsInstance(json_res, list)

        # Проверяем, имеется ли в json_res такое же количество  полей, что и в БД
        expenses = models.Expense.objects.all() #Извлекаем все объекты из БД
        self.assertEqual(len(expenses), len(json_res))

    def test_expense_create_required_fields_missing(self):
        payload = {
            'merchant': 'AT&T',
            'description': 'cell phone supscription',
            'category': 'utilities'
        }

        res = self.client.post(reverse('restapi:expense-list-create'), payload, format='json')

        self.assertEqual(400, res.status_code)