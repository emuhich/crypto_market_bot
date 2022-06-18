from asgiref.sync import sync_to_async

from admin_panel.telebot.models import Product, Client


@sync_to_async
def select_all_products():
    return Product.objects.all()


@sync_to_async()
def select_client(telegram_id):
    return Client.objects.filter(telegram_id=telegram_id)


@sync_to_async()
def create_client(username, telegram_id):
    Client.objects.get_or_create(telegram_id=telegram_id, username=username)
