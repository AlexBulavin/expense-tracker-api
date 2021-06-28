from django.test import TestCase
from restapi import models
from django.urls import reverse
from django.contrib.auth.models import User
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
    #Добавляем создание аутентифицированного запроса c credantials суперпользователя.
    def setUp(self):
        #Создаём тестового пользователя. Задаём ему тестовые параметры.
        User.objects.create_user('testUser', '', '9874563210258963214785654')
        self.client.login(username='testUser', password='9874563210258963214785654')

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

    def test_expense_retrieve(self):
        expense = models.Expense.objects.create(amount=300, merchant='George', description='loan', category='transfer')
        res = self.client.get(reverse('restapi:expense-retrieve-delete', args=[expense.id]), format='json')

        self.assertEqual(200, res.status_code)

        json_res = res.json()

        self.assertEqual(expense.id, json_res['id'])  # Проверяем, совпадают ли ID
        self.assertEqual(expense.amount, json_res['amount'])
        self.assertEqual(expense.merchant, json_res['merchant'])
        self.assertEqual(expense.description, json_res['description'])
        self.assertEqual(expense.category, json_res['category'])

    def test_expense_delete(self):
        # Создаём и вставляем с БД тестовые данные
        expense = models.Expense.objects.create(amount=400, merchant='John', description='loan', category='transfer')
        # Удаляем из БД те же самые данные, находя их по expense.id
        res = self.client.delete(reverse('restapi:expense-retrieve-delete', args=[expense.id]), format='json')

        #Первая проверка, роверяем возвращаемый код на равенство 204 (удаление)
        self.assertEqual(204, res.status_code)

        #Вторая проверка, проверяем, что запись с данными, которые мы создали и вставили больше не существует в БД
        self.assertFalse(models.Expense.objects.filter(pk=expense.id).exists())

    def test_list_expense_filter_by_merchant(self):
        #Тест на излечение из базы покупок от определенного продавца
        amazon_expense = models.Expense.objects.create(amount=100, merchant='amazon', description='sunglasses', category='fashion')
        ebay_expense = models.Expense.objects.create(amount=200, merchant='ebay', description='watch', category='fashion')

        #Создаём url к Амазоновской покупке (покупкам)
        url = '/api/expenses?merchant=amazon'
        res = self.client.get(url, format='json')

        #Проверяем статус код, есть ли ответ.
        self.assertEqual(200, res.status_code)

        json_res = res.json()

        #Поскольку в листе только 1 покупка с Амазона, то длина листа должна быть равна 1. Проверяем.
        self.assertEqual(len(json_res), 1)

        #Проверяем под каким индексом запись про покупку в Амазоне
        self.assertEqual(amazon_expense.id, json_res[0]['id'])
        self.assertEqual(amazon_expense.amount, json_res[0]['amount'])
        self.assertEqual(amazon_expense.merchant, json_res[0]['merchant'])
        self.assertEqual(amazon_expense.description, json_res[0]['description'])
        self.assertEqual(amazon_expense.category, json_res[0]['category'])

