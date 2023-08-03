from django.urls import path
from .views import ProductList, OrderList, ProductDetail

app_name = 'fastfood'
urlpatterns = [
    # path('', MainView.as_view(), name='index'),
    # path — означает путь. В данном случае путь ко всем товарам у нас останется пустым, позже станет ясно почему
    path('', ProductList.as_view()), # т.к. сам по себе это класс, то нам надо представить этот класс в виде view. Для этого вызываем метод as_view
    path('orders/', OrderList.as_view()), # т.к. сам по себе это класс, то нам надо представить этот класс в виде view. Для этого вызываем метод as_view
    path('<int:pk>', ProductDetail.as_view()),  # pk — это первичный ключ блюда, который будет выводиться у нас в шаблон
]