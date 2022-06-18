from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    title = models.CharField(
        max_length=200,
        help_text='Название новой подкатегории',
        verbose_name='Название подкатегории'
    )
    image = models.ImageField(
        'Картинка подкатегории',
        upload_to='sub_category/',
        blank=True
    )
    description = models.TextField(
        help_text='Описание категории',
        verbose_name='Описание'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']


class SubCategory(models.Model):
    title = models.CharField(
        max_length=200,
        help_text='Название новой подкатегории',
        verbose_name='Название подкатегории'
    )
    image = models.ImageField(
        'Картинка подкатегории',
        upload_to='sub_category/',
        blank=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='sub_category',
        help_text='Категория к которой относится пост',
        verbose_name='Подкатегория'
    )
    description = models.TextField(
        help_text='Описание подкатегории',
        verbose_name='Описание'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Под Категория'
        verbose_name_plural = 'Под Категории'
        ordering = ['title']


class Product(models.Model):
    name = models.CharField(
        max_length=200,
        help_text='Название нового товара',
        verbose_name='Название товара'
    )
    description = models.TextField(
        help_text='Описание',
        verbose_name='Текст Описание'
    )
    sub_category = models.ForeignKey(
        SubCategory,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='products',
        help_text='Подкатегория к которой относится пост',
        verbose_name='Подкатегория'
    )
    image = models.ImageField(
        'Картинка продукта',
        upload_to='products/',
        blank=True
    )
    price = models.IntegerField(
        help_text='Цена продукта',
        verbose_name='Цена'
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Продукты'
        verbose_name_plural = 'Продукты'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.name
