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
        'status'
    )

    list_display_links = ('pk', 'product', 'customer')
    empty_value_display = '-пусто-'

    class Meta:
        verbose_name_plural = 'Заказы'


admin.site.register(Product, ProductAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Orders, OrdersAdmin)
admin.site.site_title = 'Админ панель телеграмм бота'
admin.site.site_header = 'Админ панель телеграмм бота'
