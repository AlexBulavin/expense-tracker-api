#from django.test import TestCase
from unittest import TestCase

# Create your tests here.
# Предположм, что мы имеем для тестирования функцию, которая на вход получает два арнумента, а на выходе выдаёт их сумму
def two_integers_sum(a, b):
    return a+b+10

class TestSum(TestCase):
    def test_sum(self):
        # Проверяем на конкретном примере, если результат выполнения функции two_integers_sum(1,2) равен 3
        self.assertEqual(two_integers_sum(1, 2), 3)
