from django.db import models

# Create your models here.


class Services(models.Model):
    shipping_cost = models.IntegerField(default=0, verbose_name="Стоимость доставки")
    status = models.IntegerField(default=0, verbose_name="Статус")

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'


    def __int__(self):
        return self.shipping_cost