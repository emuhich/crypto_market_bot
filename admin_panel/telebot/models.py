import os

import requests
from aiogram.utils.markdown import hbold
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save, post_init
from dotenv import load_dotenv

load_dotenv()
User = get_user_model()
BOT_TOKEN = str(os.getenv("BOT_TOKEN"))


class CreatedModel(models.Model):
    """Абстрактная модель. Добавляет дату создания."""
    created = models.DateTimeField(
        'Дата создания',
        auto_now_add=True
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата изменения")

    class Meta:
        abstract = True


class Category(models.Model):
    title = models.CharField(
        max_length=200,
        help_text='Название новой категории',
        verbose_name='Название категории'
    )
    image = models.CharField(
        max_length=200,
        help_text='Ссылка на картинку категории',
        verbose_name='Картинка'
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
    image = models.CharField(
        max_length=200,
        help_text='Ссылка на картинку подкатегории',
        verbose_name='Картинка'
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

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Под Категория'
        verbose_name_plural = 'Под Категории'
        ordering = ['title']


class Product(CreatedModel):
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
        help_text='Подкатегория к которой относится подкатегория',
        verbose_name='Подкатегория'
    )
    image = models.CharField(
        max_length=200,
        help_text='Ссылка на картинку товара',
        verbose_name='Картинка'
    )
    cost_price = models.IntegerField(
        help_text='Себестоимость продукта в USDT',
        verbose_name='Себестоимость',
        blank=True,
        null=True
    )
    price = models.IntegerField(
        help_text='Цена продукта в USDT',
        verbose_name='Цена'
    )
    quantity = models.IntegerField(
        help_text='Количетсво продукта',
        verbose_name='Количество',
        default=0
    )

    class Meta:
        verbose_name = 'Продукты'
        verbose_name_plural = 'Продукты'
        ordering = ('-created',)

    def __str__(self):
        return self.name


class Client(CreatedModel):
    username = models.CharField(
        max_length=50,
        help_text='Юзернейм клиента',
        verbose_name='Юзернейм'
    )
    phone = models.CharField(
        max_length=50,
        help_text='Номер телефона клиента',
        verbose_name='Номер телефона',
        blank=True,
        null=True
    )
    full_name = models.CharField(
        max_length=50,
        help_text='ФИО клиента',
        verbose_name='ФИО',
        blank=True,
        null=True
    )
    address = models.TextField(
        help_text='Адрес клиента',
        verbose_name='Адрес',
        blank=True,
        null=True
    )
    telegram_id = models.BigIntegerField(
        help_text='Telegram ID пользователя',
        verbose_name='Telegram ID'
    )

    class Meta:
        verbose_name = 'Клиенты телеграмм бота'
        verbose_name_plural = 'Клиенты телеграмм бота'
        ordering = ('-created',)

    def __str__(self):
        return self.username


class Orders(CreatedModel):
    previous_state = None

    THEME_CHOICES = (
        ('accepted', 'принят в обработку'),
        ('processed', 'обработан'),
        ('in_delivery', 'передан в доставку'),
        ('delivered', 'доставлен'),
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='product',
        help_text='Товар который заказал клиент',
        verbose_name='Товар'
    )
    customer = models.ForeignKey(
        Client,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='customer',
        help_text='Заказчик',
        verbose_name='Заказчик'
    )
    address = models.TextField(
        help_text='Адрес клиента',
        verbose_name='Адрес',
        blank=True,
        null=True
    )
    phone = models.CharField(
        max_length=50,
        help_text='Номер телефона клиента',
        verbose_name='Номер телефона',
        blank=True,
        null=True
    )
    quantity = models.IntegerField(
        help_text='Количетсво продукта',
        verbose_name='Количество',
        default=1
    )
    price = models.IntegerField(
        help_text='Сумма заказа в USDT',
        verbose_name='Сумма'
    )
    cost_price = models.IntegerField(
        help_text='Себестоимость заказа в USDT',
        verbose_name='Себестоимость',
        blank=True,
        null=True
    )

    status = models.CharField(
        choices=THEME_CHOICES,
        default='accepted',
        max_length=40,
        help_text='Статус заказа',
        verbose_name='Статус',
    )

    @staticmethod
    def post_save(sender, instance, created, **kwargs):
        if instance.previous_state != instance.status:
            if instance.status == 'accepted':
                status = "принят в обработку"
            elif instance.status == 'processed':
                status = "обработан"
            elif instance.status == 'in_delivery':
                status = "передан в доставку"
            else:
                status = "доставлен"

            requests.get(
                f"https://api.telegram.org/bot{BOT_TOKEN}/"
                f"sendMessage?chat_id={instance.customer.telegram_id}&text="
                f"{hbold('Статус вашего заказа:')} {instance.product.name}, {hbold(f'изменен на «{status}»')},&parse_mode=html"
            )

    @staticmethod
    def remember_state(sender, instance, **kwargs):
        instance.previous_state = instance.status

    class Meta:
        verbose_name = 'Заказы'
        verbose_name_plural = 'Заказы'
        ordering = ('-created',)

    def __str__(self):
        return self.product.name


class Questions(CreatedModel):
    questions = models.CharField(
        max_length=50,
        help_text='Часто задоваемый вопрос',
        verbose_name='Вопрос',
    )
    answer = models.TextField(
        help_text='Ответ на ваш вопрос',
        verbose_name='Ответ',
    )

    class Meta:
        verbose_name = 'Часто задаваемые вопросы'
        verbose_name_plural = 'Часто задаваемые вопросы'
        ordering = ('-created',)

    def __str__(self):
        return self.questions


class TokenBinance(models.Model):
    token = models.CharField(
        max_length=100,
        help_text='Токен для binance',
        verbose_name='Токен',
    )
    secret_key = models.CharField(
        max_length=100,
        help_text='Секретный ключ для binance',
        verbose_name='Секретный ключ',
    )

    class Meta:
        verbose_name = 'Ключи для доступа к оплате'
        verbose_name_plural = 'Ключи для доступа к оплате'

    def __str__(self):
        return self.token


class BinanceOperationId(models.Model):
    txId = models.CharField(
        max_length=300,
        help_text='Уникальный ID платежа',
        verbose_name='ID платежка',
        unique=True
    )

    def __str__(self):
        return self.txId


post_save.connect(Orders.post_save, sender=Orders)
post_init.connect(Orders.remember_state, sender=Orders)
