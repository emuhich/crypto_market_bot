from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


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
    price = models.IntegerField(
        help_text='Цена продукта',
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
    quantity = models.IntegerField(
        help_text='Количетсво продукта',
        verbose_name='Количество',
        default=1
    )
    status = models.CharField(
        choices=THEME_CHOICES,
        default='accepted',
        max_length=40,
        help_text='Статус заказа',
        verbose_name='Статус',
    )

    class Meta:
        verbose_name = 'Заказы'
        verbose_name_plural = 'Заказы'
        ordering = ('-created',)

    def __str__(self):
        return self.product.name
