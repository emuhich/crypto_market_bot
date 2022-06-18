from asgiref.sync import sync_to_async

from admin_panel.telebot.models import Product


@sync_to_async
def select_all_products():
    return Product.objects.all()
