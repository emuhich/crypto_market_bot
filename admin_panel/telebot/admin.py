from django.contrib import admin

from django.utils.safestring import mark_safe

from .models import Product, SubCategory, Category, Client, Orders


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
    fields = ('name', 'description', 'sub_category', 'image', 'get_html_image', 'price', 'quantity')
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
        'get_address',
        'status',
        'get_status_emoji',
    )

    list_display_links = ('pk', 'product',)
    list_editable = ('status',)
    list_filter = ('status',)

    empty_value_display = '-пусто-'

    def get_address(self, object):
        return object.customer.address

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

    get_address.short_description = "Адрес отправки"

    class Meta:
        verbose_name_plural = 'Заказы'


admin.site.register(Product, ProductAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Orders, OrdersAdmin)
admin.site.site_title = 'Админ панель телеграмм бота'
admin.site.site_header = 'Админ панель телеграмм бота'
