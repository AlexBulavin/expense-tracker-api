from django.db import models

# Create your models here.
class Expense(models.Model):
    amount = models.FloatField()
    merchant = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    # После создания модели необходимо запустить команды python manage.py makemigrations
    # И python manage.py migrate.
    # Также запушить в Git изменения в файле/лах миграции папки migrations. Иначе тесты на GitHub не пройдут.



