from django.contrib import admin

# Register your models here.
from django.utils.safestring import mark_safe

from .models import Product, SubCategory, Category


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'sub_category',
        'get_html_image',
        'price',
    )
    list_editable = ('sub_category',)
    search_fields = ('name',)
    list_filter = ('pub_date', 'sub_category',)
    empty_value_display = '-пусто-'

    def get_html_image(self, object):
        if object.image:
            return mark_safe(f"<img src='{object.image.url}'> width=50")

    class Meta():
        verbose_name_plural = 'Продукты'


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'title',
        'category',
        'description',
    )
    empty_value_display = '-пусто-'
    list_filter = ('category',)
    search_fields = ('title',)

    class Meta():
        verbose_name_plural = 'Под категории'


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'title',
        'description',
    )
    empty_value_display = '-пусто-'
    search_fields = ('title',)

    class Meta():
        verbose_name_plural = 'Категории'


admin.site.register(Product, ProductAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.site_title = 'Админ панель телеграмм бота'
admin.site.site_header = 'Админ панель телеграмм бота'
