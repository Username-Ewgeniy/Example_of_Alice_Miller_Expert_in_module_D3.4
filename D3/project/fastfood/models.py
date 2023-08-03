from django.db import models
from datetime import datetime
from django.core.validators import MinValueValidator


class Order(models.Model): 
    time_in = models.DateTimeField(auto_now_add=True)
    time_out = models.DateTimeField(auto_now=True)
    cost = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    staff = models.ForeignKey('Staff', on_delete=models.CASCADE)
    take_away = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)
    product = models.ManyToManyField('Product', through='ProductOrder')
    
    def __str__(self):
        return f'Order #{self.pk} - Total: {self.cost}'
    @property
    def total(self):
        sum = self.product.aggregate(sum=models.Sum('price'))['sum']
        self.cost = sum
        self.save()
        return sum
    def finish_order(self):
        self.time_out = datetime.now()
        self.complete = True
        self.save() 

class Product(models.Model):
    DRINK = 'DRNK'
    BURGER = 'BRGR'
    SNACK = 'SNCK'
    DESSERT = 'DSRT'

    TYPE_CHOICES = [
        (DRINK, 'Drink'),
        (BURGER, 'Burger'),
        (SNACK, 'Snack'),
        (DESSERT, 'Dessert'),
    ]
    type = models.CharField(max_length=5, choices=TYPE_CHOICES, default=BURGER)
    name = models.CharField(
        max_length=255, 
        unique=True
        )
    price = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        )
    description = models.TextField()
    
    def __str__(self):
        return f'Product #{self.pk} - Name: {self.name}'
    

class Staff(models.Model):
    WAITER = 'WTR'
    CASHIER = 'CSHR'
    JANITOR = 'JNTR'
    MANAGER = 'MNGR'
    ADMIN = 'ADMN'

    POSITION_CHOICES = (
        (WAITER, 'Waiter'),
        (CASHIER, 'Cashier'),
        (JANITOR, 'Janitor'),
        (MANAGER, 'Manager'),
        (ADMIN, 'Admin'),
    )
    position = models.CharField(max_length=5, choices=POSITION_CHOICES, default=WAITER)
    full_name = models.CharField(max_length=255)
    labor_contract = models.IntegerField(default=0)
    
    def __str__(self):
        return f'Staff #{self.pk} - Position: {self.position}'

    class Meta:
        verbose_name = 'Staff'
        verbose_name_plural = 'Staff'

class ProductOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    _amount = models.SmallIntegerField(default=1)

    def __str__(self):
        return f'Order #{self.order.pk} - Product: {self.product.name} x {self.amount}'
    
    def product_sum(self):
        product_price = self.product.price
        return product_price * self.amount   
    
    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        self._amount = int(value) if value >= 0 else 0
        self.save()