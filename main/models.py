from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.


class Services(models.Model):
    shipping_cost = models.IntegerField(default=0, verbose_name="Стоимость доставки")
    status = models.IntegerField(default=0, verbose_name="Статус")

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'



    def __int__(self):
        return self.shipping_cost

class Order(models.Model):
    name = models.CharField(max_length=200, verbose_name='Имя')
    address = models.CharField(max_length=200, verbose_name='Адрес')
    phone_number = models.CharField(max_length=200, verbose_name='Номер телефона')
    desc = RichTextField(blank=True,  verbose_name='Описание')
    status = models.IntegerField(default=0,verbose_name="Статус")

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return self.name