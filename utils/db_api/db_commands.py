from asgiref.sync import sync_to_async
from django.shortcuts import get_object_or_404

from admin_panel.telebot.models import Product, Client, Questions, Category, SubCategory, TokenBinance, Orders


@sync_to_async
def select_all_products():
    return Product.objects.all()


@sync_to_async()
def select_client(telegram_id):
    return Client.objects.get(telegram_id=telegram_id)


@sync_to_async()
def check_client(telegram_id):
    return Client.objects.filter(telegram_id=telegram_id).exists()


@sync_to_async()
def create_client(username, telegram_id):
    Client.objects.get_or_create(telegram_id=telegram_id, username=username)


@sync_to_async
def select_all_questions():
    return Questions.objects.all()


@sync_to_async
def get_question(pk):
    return get_object_or_404(Questions, pk=pk)


@sync_to_async
def update_client_info(telegram_id, fio=None, address=None, phone=None):
    user = Client.objects.get(telegram_id=telegram_id)
    if fio:
        user.full_name = fio
        user.save(update_fields=["full_name"])
        return user
    if address:
        user.address = address
        user.save(update_fields=["address"])
        return user
    if phone:
        user.phone = phone
        user.save(update_fields=["phone"])
        return user


@sync_to_async
def get_all_category():
    return Category.objects.all()


@sync_to_async
def get_category(pk):
    return Category.objects.get(pk=pk)


@sync_to_async
def get_sub_categories(pk):
    category = Category.objects.get(pk=pk)
    return category.sub_category.all()


@sync_to_async
def get_sub_category(pk):
    return SubCategory.objects.get(pk=pk)


@sync_to_async
def get_products(pk):
    sub_category = SubCategory.objects.get(pk=pk)
    return sub_category.products.exclude(quantity=0)


@sync_to_async
def get_product(pk):
    return Product.objects.get(pk=pk)


@sync_to_async
def get_binance_key():
    obj_list = TokenBinance.objects.all()
    client = obj_list[0]
    return client.token, client.secret_key


@sync_to_async()
def create_order(pk, telegram_id, quantity):
    product = Product.objects.get(pk=pk)
    product.quantity -= quantity
    product.save()
    client = Client.objects.get(telegram_id=telegram_id)
    order = Orders()
    order.product = product
    order.customer = client
    order.address = client.address
    order.phone = client.phone
    order.quantity = quantity
    order.price = product.price * quantity
    order.status = 'accepted'
    if product.cost_price:
        order.cost_price = product.cost_price * quantity
    order.save()


@sync_to_async()
def get_orders_by_user_id(telegram_id):
    user = Client.objects.get(telegram_id=telegram_id)
    return user.customer.all().order_by('-updated')


@sync_to_async()
def get_order(pk):
    return Orders.objects.get(pk=pk)
