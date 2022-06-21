from django.contrib import admin
from django.contrib.auth.models import Group

from django.utils.safestring import mark_safe

from .models import Product, SubCategory, Category, Client, Orders, Questions, TokenBinance


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'sub_category',
        'get_html_image',
        'price',
        'quantity'
    )
    list_display_links = ('pk', 'name')
    list_editable = ('sub_category',)
    search_fields = ('name',)
    list_filter = ('created', 'sub_category',)
    empty_value_display = '-пусто-'
    fields = ('name', 'description', 'sub_category', 'image', 'get_html_image', 'price', 'cost_price', 'quantity')
    readonly_fields = ('created', 'get_html_image')

    def get_html_image(self, object):
        if object.image:
            return mark_safe(f"<img src='{object.image}' width=50>")

    get_html_image.short_description = "Изображение"

    class Meta:
        verbose_name_plural = 'Продукты'


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'title',
        'category',
        'get_html_image',
    )

    list_display_links = ('pk', 'title')
    empty_value_display = '-пусто-'
    list_editable = ('category',)
    list_filter = ('category',)
    search_fields = ('title',)

    def get_html_image(self, object):
        if object.image:
            return mark_safe(f"<img src='{object.image}' width=50>")

    get_html_image.short_description = "Изображение"

    class Meta:
        verbose_name_plural = 'Под категории'


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'title',
        'get_html_image',
    )

    list_display_links = ('pk', 'title')
    empty_value_display = '-пусто-'
    search_fields = ('title',)

    def get_html_image(self, object):
        if object.image:
            return mark_safe(f"<img src='{object.image}' width=50>")

    get_html_image.short_description = "Изображение"

    class Meta:
        verbose_name_plural = 'Категории'


class ClientAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'phone',
        'telegram_id'
    )

    list_display_links = ('pk', 'username')
    empty_value_display = '-пусто-'
    search_fields = ('username',)

    class Meta:
        verbose_name_plural = 'Клиенты Крипто Маркета'


class OrdersAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'product',
        'customer',
        'quantity',
        'address',
        'price',
        'phone',
        'status',
        'get_status_emoji',
    )

    list_display_links = ('pk', 'product',)
    list_editable = ('status',)
    list_filter = ('status',)

    empty_value_display = '-пусто-'

    def get_status_emoji(self, object):
        if object.status == "accepted":
            return mark_safe(f"&#128308;")
        elif object.status == "processed":
            return mark_safe(f"&#128992;")
        elif object.status == "in_delivery":
            return mark_safe(f"&#128993;")
        elif object.status == "delivered":
            return mark_safe(f"&#128994;")

    get_status_emoji.short_description = ""

    class Meta:
        verbose_name_plural = 'Заказы'


class QuestionsAdmin(admin.ModelAdmin):
    list_display = (
        'questions',
        'answer',
    )

    list_display_links = ('questions',)
    empty_value_display = '-пусто-'
    search_fields = ('questions',)

    class Meta:
        verbose_name_plural = 'Часто задаваемые вопросы'


class TokenBinanceAdmin(admin.ModelAdmin):
    list_display = (
        'token',
        'secret_key',
    )

    list_display_links = ('token',)
    empty_value_display = '-пусто-'
    search_fields = ('token',)

    class Meta:
        verbose_name_plural = 'Ключи для доступа к оплате'


class ServiceAdmin(admin.ModelAdmin):
    change_form_template = "base.html"

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['users_count'] = Client.objects.all().count()
        return super(ServiceAdmin, self).add_view(request, form_url, extra_context)


admin.site.register(Product, ProductAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Orders, OrdersAdmin)
admin.site.register(Questions, QuestionsAdmin)
admin.site.register(TokenBinance, TokenBinanceAdmin)
admin.site.site_title = 'Админ панель телеграмм бота'
admin.site.site_header = 'Админ панель телеграмм бота'
