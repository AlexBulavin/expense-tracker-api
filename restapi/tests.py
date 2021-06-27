from django.test import TestCase
from restapi import models
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
        self.assertEqual(b'amazon', inserted_expense.merchant)
        self.assertEqual(b'anc headphones', inserted_expense.description)
        self.assertEqual(b'music', inserted_expense.category)


