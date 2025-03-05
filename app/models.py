from django.db import models
from account.models import CustomUser

class Category(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        null = True,
        blank = True
    )
    name = models.CharField(
        max_length=255,
        verbose_name="カテゴリ名"
    )
    def __str__(self):
        return self.name

class Post(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE) 
    date = models.DateField(
        verbose_name="日付"
    )
    name = models.CharField(
        max_length=255,
        verbose_name="支出名"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null = True,
        verbose_name="カテゴリ名"
    )
    price = models.PositiveIntegerField(
        default = 0,
        verbose_name = "値段"
    )
    def __str__(self):
        return f"{self.name} : {self.price}円"

