from django.urls import path
from restapi import views


urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('api/', include('restapi.urls', 'restapi'), namespace='restapi')
    path('expenses/', views.ExpenseListCreate.as_view(), name='expense-list-create')
]
